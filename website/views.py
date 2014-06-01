from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from paypal.driver import PayPal
from revelation_ink import settings
from revelation_ink.logger import logger
from clothing.models import Item, Size, StockSold, Transaction
from website.models import AboutPagePhoto, FrontPagePhoto
from decimal import Decimal
import copy, uuid
try:
  import json
except:
  import simplejson as json
def backbone_ex(request):
  return render_to_response("backbone/index.html", {})

def shipping_guide(request):
  return render_to_response("website/shipping.html", {})

def privacy_policy(request):
  return render_to_response("website/privacy.html", {})

def home(request):
  photos = FrontPagePhoto.objects.order_by("weight")
  image_list = [p.image.url for p in photos] 
  return render_to_response("website/index.html", 
    {
      "image_list" : image_list,
      "paypal_debug" : settings.PAYPAL_DEBUG,
    })

def home_new(request):
  guys_list = Item.objects.filter(category__parent__name="Guys", shown=True)
  girls_list = Item.objects.filter(category__parent__name="Girls", shown=True)
  return render_to_response("website/index_new.html", 
    {
      "product_lists" : {
         "Guys": guys_list,
         "Girls" : girls_list,
      },
      "paypal_debug" : settings.PAYPAL_DEBUG,
    })

def about(request):
  photos = AboutPagePhoto.objects.order_by("weight")
  image_list = [p.image for p in photos] 
  return render_to_response("website/about.html", 
    {
      "image_list" : image_list,
      "paypal_debug" : settings.PAYPAL_DEBUG,
    })

def get_cart(request):
  cart = request.session.get("cart",[])
  return HttpResponse(content=json.dumps(cart))

def get_cart_session(request):
  try:
    #Return cart OR an empty list
    return request.session.get("cart",[])
  except Exception, e:
    logger.error("Session failure")
    logger.error(e)
    return HttpResponse(status=500, content="Internal Server Failure")

def test_post_item(request):
  try:
    #Add the new item to cart
    item_id = request.POST["id"]
    name = request.POST["name"]
    size = request.POST["size"]
    quantity = request.POST["quantity"]
    return (item_id, name, size, quantity)
  except Exception, e:
    logger.error(e)
    return HttpResponse(status=400, content="Bad params passed, expects id, name, size & quantity")

def collect_billing_info(request):
  logger.info(request)
  c = RequestContext(request, {})
  return render_to_response("website/checkout/billing_info.html", c)
  
def getCardArgs(querydict, *args, **kwargs):
  if len(querydict["fullname-card"]) > 0 and len( querydict["fullname-card"].split(" ",1) ) > 1:
    first_name = querydict["fullname-card"].split(" ",1)[0]
    last_name = querydict["fullname-card"].split(" ",1)[1]
  else:
    first_name,last_name = "",""
  return {
    "acct":querydict["ccnumber-card"],
    "expdate":"%s%s" % (querydict["month-expire-card"],querydict["year-expire-card"]),
    "cvv2":querydict["cvn-card"],
    "cardtype":querydict["type-card"],
    "first_name":first_name,
    "last_name":last_name,
  } 
"""
{
 u"csrfmiddlewaretoken": [u"5GLWXLj8HYGFaR9m4SRjWPxW4me46v9X"],

 u"lastname-shipping": [u""],
 u"address-shipping": [u""],
 u"country-shipping": [u"United States"],
 u"zip-shipping": [u""],
 u"city-shipping": [u""],
 u"address2-shipping": [u""],
 u"firstname-shipping": [u""],

 u"lastname-billing": [u"Gregory"],
 u"zip-billing": [u"85704"],
 u"city-billing": [u"Tucson"],
 u"address-billing": [u"641 E Windward Cir"],
 u"country-billing": [u"United States"],
 u"firstname-billing": [u"Steve"],
 u"address2-billing": [u""],
 u"State": [u"AZ", u""],
 u"cancel": [u""],
}
"""
def getBillingArgs(querydict):
  return {
    "street":querydict["address-billing"] if querydict.get("address2-billing",None) else "%s\n%s" % (querydict["address-billing"],querydict["address2-billing"]),
    "city":querydict["city-billing"],
    "state":querydict["state-billing"],
    "countrycode":"US",
    "zip":querydict["zip-billing"],
    "first_name":querydict["firstname-billing"],
    "last_name":querydict["lastname-billing"],
    "email":querydict["email-billing"],
  } 

def getShippingArgs(querydict, billing_args):
  """
  Get shipping args (Use billing if missing..)
  """
  if "yes" in querydict.get("ship_to_billing",[]):
    return copy.copy(billing_args)

  return {
    "street":querydict.get("address-shipping",querydict.get("address-billing")) if querydict.get("address2-shipping",None) else "%s\n%s" % (querydict.get("address-shipping",querydict.get("address-billing")),querydict.get("address2-shipping")),
    "city":querydict.get("city-shipping",querydict.get("city-billing")),
    "state":querydict.get("state-shipping",querydict.get("state-billing")),
    "countrycode":"US",
    "zip":querydict.get("zip-shipping",querydict.get("zip-billing")),
    "first_name":querydict["firstname-shipping"],
    "last_name":querydict["lastname-shipping"],
    "email":querydict["email-shipping"],
  }

def purchase_complete(request): 

  (cart_list, pretax_total, tax, amountTaxed, shipping_total, total) = get_cart_details(request)

  card_args = getCardArgs(request.POST)
  billing_args = getBillingArgs(request.POST)
  shipping_args = getShippingArgs(request.POST, billing_args)
  #Create the order model 
  logger.warn(card_args)
  logger.warn(billing_args)
  p = PayPal()
  result = p.DoDirectPayment(*card_args, **billing_args)
  #Update the order to show payment went through
  #show the entire order on the next page
  return render_to_response("website/cart_purchased.html", 
    {
      "cart_list" : cart_list,
      "cart_pretax" : "%.2f" % round(pretax_total,2),
      "cart_tax" : "%.1f" % round(tax*100,1),
      "cart_tax_total" : "%.2f" % round(amountTaxed,2),
      "shipping_total" : "%.2f" % round(shipping_total,2),
      "cart_total" : "%.2f" % round(total,2),
    })

def getCartList(request):
  cart_list = []
  cart = get_cart_session(request)
  cartTotal = 0
  for cart_item in cart:
    item = Item.objects.get(id=cart_item["id"])
    itemPrice = item.markdownPrice if item.markdownPrice else item.price
    total = itemPrice * int(cart_item["quantity"])
    cartTotal = cartTotal + total
    cart_list.append({
	"id": cart_item["id"],
	"size": cart_item["size"],
	"image_url": item.front.url,
	"price": "%.2f" % round(itemPrice,2),
	"total": "%.2f" % round(total,2),
	"quantity": cart_item["quantity"],
	"description": item.description,
	})
  return (cart_list,cartTotal)
#Dead Paypal v1 shit
#def reviewTransaction(request):
#  logger.info(request)
#  (cart_list,cartTotal) = getCartList(request)
#  request.session["paypal_PayerID"] = request.GET["PayerID"]
#  request.session["paypal_token"] = request.GET["token"]
#  return render_to_response("website/review_transaction.html", 
#    {
#      "cart_list" : cart_list,
#      "cart_total" : "%.2f" % round(cartTotal,2),
#      "paypal_debug" : settings.PAYPAL_DEBUG,
#    })
#  #Show modal dialog on its own screen
#  #On "OKAY" click "DoExpressCheckoutPayment"
#
#def completeTransaction(request):
#  logger.info(request)
#  #Clear the cart
#  (cart_list,cartTotal) = getCartList(request)
#  p = PayPal()
#  cartTotal = request.session["paypal_total"]
#  p.DoExpressCheckoutPayment("USD", "%.2f" % round(cartTotal,2), request.session["paypal_token"], request.session["paypal_PayerID"])
#  #Test "status == ok"
#  #Create a new transaction
#  p.GetExpressCheckoutDetails(settings.SERVER_URL+"cart/review/", settings.SERVER_URL, request.session["paypal_token"])
#  name = "%s %s" % (p.api_response["FIRSTNAME"],p.api_response["LASTNAME"])
#  email = p.api_response["EMAIL"]
#  #"Address\n\nTucson,AZ 85704"
#  address = "%s\n%s\n%s,%s %s" % (p.api_response.get("SHIPTOSTREET","No Street Info"), p.api_response.get("SHIPTOSTREET2",""), p.api_response.get("SHIPTOCITY","No City"), p.api_response.get("SHIPTOSTATE","NoState"), p.api_response.get("SHIPTOZIP","No ZIP"))
#  #Remove the cart and paypal variables
#  transaction = Transaction(full_name=name, email=email, shipping_info=address)
#  transaction.save()
#  for list_item in cart_list:
#    item = Item.objects.get(id=list_item["id"])
#    size = Size.objects.get(name=list_item["size"])
#    sold_item = StockSold(item=item, size=size, count=list_item["quantity"])
#    sold_item.save()
#    transaction.items_sold.add(sold_item)
#  return transaction.confirmation_id

def make_transaction(full_name, email, shipping_addr, billing_addr, cart_list):
  transaction = Transaction(full_name=full_name, email=email, shipping_info=shipping_addr, billing_info=billing_addr)
  transaction.confirmation_id = uuid.uuid4()
  transaction.save()
  for list_item in cart_list:
    item = Item.objects.get(id=list_item["id"])
    size = Size.objects.get(name=list_item["size"])
    sold_item = StockSold(item=item, size=size, count=list_item["quantity"])
    sold_item.save()
    transaction.items_sold.add(sold_item)
  return transaction.confirmation_id


def reviewTransaction(request):
  """
  Expects the POST form from /checkout/collect/
  """
  logger.info(request)
  if request.method != "POST":
    #Got here by accident.. Go back to the cart
    return HttpResponseRedirect("/cart/show/")
  #User pressed cancel, send them to the shop
  if "cancel" in request.POST.get("submit","cancel"):
    return HttpResponseRedirect("/shop/")
  #Assert: We have a form full of user data that needs to go back to the next page!
  #if reviewed and ready to complete, run:
  #return completeTransaction(request)
  if "purchase" in request.POST.get("submit"):
    return make_purchase(request)
  else:
    return show_review_page(request)
  #Show modal dialog on its own screen
  #On "OKAY" click "DoExpressCheckoutPayment"

def show_review_page(request, errors=[]):
    (cart_list,pretax_total, tax, tax_amount, shipping_amount, total) = get_cart_details(request)
    card_args = getCardArgs(request.POST)
    card_args["last4"] = card_args["acct"][-4:] if len(card_args["acct"]) > 4 else ""
    billing_args = getBillingArgs(request.POST)
    shipping_args = getShippingArgs(request.POST, billing_args)
    billing_full_name = "%s %s" % (billing_args["first_name"], billing_args["last_name"])
    billing_addr = "%s\n%s,%s %s" % (billing_args["street"], billing_args["city"], billing_args["state"], billing_args["zip"])
    shipping_full_name = "%s %s" % (shipping_args["first_name"], shipping_args["last_name"])
    shipping_addr = "%s\n%s,%s %s" % (shipping_args["street"], shipping_args["city"], shipping_args["state"], shipping_args["zip"])
    card_full_name = "%s %s" % (card_args["first_name"], card_args["last_name"])
    logger.info(card_full_name)
    logger.info(card_args["last4"])
    logger.info(shipping_args["email"])
    logger.info(billing_args["email"])
    c = RequestContext(request, {
        "shipping" : {
            "full_name": shipping_full_name,
            "address": shipping_addr,
            "email": shipping_args["email"],
        },
        "billing" : {
            "full_name": billing_full_name,
            "address": billing_addr,
            "email": billing_args["email"],
        },
        "card" : {
            "full_name": card_full_name,
            "last4": card_args["last4"],
            "type": card_args["cardtype"]
        },
        "server_url": settings.SERVER_URL,
        "post_params":request.POST.copy(), 
        "cart_list":cart_list,
        "cart_pretax" : "%.2f" % round(pretax_total,2),
        "cart_tax" : "%.1f" % round(tax*100,1),
        "cart_tax_total" : "%.2f" % round(tax_amount,2),
        "shipping_total" : "%.2f" % round(shipping_amount,2),
        "cart_total" : "%.2f" % round(total,2),
        "validation_errors": errors,
        })
    return render_to_response("website/checkout/review_payment.html", c)

def make_purchase(request):
    (cart_list,pretax_total, tax, tax_amount, shipping_total, total) = get_cart_details(request)
    card_args = getCardArgs(request.POST)
    billing_args = getBillingArgs(request.POST)
    shipping_args = getShippingArgs(request.POST, billing_args)

    error_list = []

    first_name = billing_args.pop("first_name")
    if not first_name:
        error_list.append("First name missing from billing addresss")

    last_name = billing_args.pop("last_name")
    if not last_name:
        error_list.append("Last name missing from billing addresss")

    card_args["amount"] = Decimal(total)
    billing_args["ipaddress"] = request.META["REMOTE_ADDR"]

    full_name = "%s %s" % (shipping_args["first_name"], shipping_args["last_name"])
    billing_addr = "%s\n%s,%s %s" % (billing_args["street"], billing_args["city"], billing_args["state"], billing_args["zip"])
    shipping_addr = "%s\n%s,%s %s" % (shipping_args["street"], shipping_args["city"], shipping_args["state"], shipping_args["zip"])
    email = shipping_args["email"]
    if not email:
        error_list.append("Please enter an e-mail address")

    p = PayPal()
    card_tuple = (card_args["acct"], card_args["expdate"], card_args["cvv2"], card_args["cardtype"], card_args["first_name"], card_args["last_name"], card_args["amount"])
    if error_list:
        return show_review_page(request, errors=error_list)

    result = p.DoDirectPayment(*card_tuple, **billing_args)
    if not result:
        error_list.append("Your Credit Card was not accepted! Please review your information and try again.")
        return show_review_page(request, errors=error_list)
    confirm_id = make_transaction(full_name, email, shipping_addr, billing_addr, cart_list)
    #send_confirmation_email(full_name, email)
    params = {
        "cart_list" : cart_list,
        "transaction_id" : confirm_id,
        "cart_pretax" : "%.2f" % round(pretax_total,2),
        "cart_tax" : "%.1f" % round(tax*100,1),
        "cart_tax_total" : "%.2f" % round(tax_amount, 2),
        "shipping_total" : "%.2f" % round(shipping_total, 2),
        "cart_total" : "%.2f" % round(total,2),
        "server_url": settings.SERVER_URL,
        "billing_info":billing_args,
        "card_info":card_args,
        "shipping_info":shipping_args,
      }
    logger.info(params)
    c = RequestContext(request, params)
    return render_to_response("website/thank_you_transaction.html",c)

    
def send_email(subject, body, from_email, to, cc=None, fail_silently=False):
    """ Use django.core.mail.EmailMessage to send and log an Atmosphere email.
    """
    try:
        msg = EmailMessage(subject=subject, body=body, 
                           from_email=from_email,
                           to=to,
                           cc=cc)
        msg.send(fail_silently=fail_silently)
        email_logger.info("Email Sent. To: %s\nFrom: %sCc: %s\nSubject: %s\nBody:\n%s" %
                         (from_email,
                          to,
                          cc,
                          subject,
                          body))
        return True
    except Exception as e:
        logger.error(e)
        return False

def get_cart_details(request):
  (cart_list,pretax_total) = getCartList(request)
  pretax_total = float(pretax_total)
  (tax, amountTaxed) = get_tax_total(pretax_total)
  shipping_total = get_shipping_total(cart_list)
  total = amountTaxed + pretax_total + shipping_total
  return (cart_list, pretax_total, tax, amountTaxed, shipping_total, total)

#def completeTransaction(request):
#  logger.info(request)
#  #Clear the cart
#  (cart_list,cartTotal) = getCartList(request)
#  p = PayPal()
#  cartTotal = request.session["paypal_total"]
#  p.DoExpressCheckoutPayment("USD", "%.2f" % round(cartTotal,2), request.session["paypal_token"], request.session["paypal_PayerID"])
#  #Test "status == ok"
#  #Create a new transaction
#  p.GetExpressCheckoutDetails(settings.SERVER_URL+"cart/review/", settings.SERVER_URL, request.session["paypal_token"])
#  name = "%s %s" % (p.api_response["FIRSTNAME"],p.api_response["LASTNAME"])
#  email = p.api_response["EMAIL"]
#  #"Address\n\nTucson,AZ 85704"
#  address = "%s\n%s\n%s,%s %s" % (p.api_response.get("SHIPTOSTREET","No Street Info"), p.api_response.get("SHIPTOSTREET2",""), p.api_response.get("SHIPTOCITY","No City"), p.api_response.get("SHIPTOSTATE","NoState"), p.api_response.get("SHIPTOZIP","No ZIP"))
#  #Remove the cart and paypal variables
#  #transaction.save()
#  del request.session["cart"] 
#  del request.session["paypal_PayerID"] 
#  del request.session["paypal_token"] 
#	{
#	  "cart_list" : cart_list,
#	  "cart_total" : "%.2f" % round(cartTotal,2)
#	})

def update_cart(request):
  cart = get_cart_session(request)
  (item_id, name, size, quantity) = test_post_item(request)
  try:
    item = Item.objects.get(id=item_id)
    logger.debug(cart)
    for cart_item in cart:
      #If item in cart matches ID and size
      if cart_item["id"] == item_id and cart_item["size"] == size:
        cart_item["quantity"] = quantity
    cart = [item for item in cart if item["quantity"] != "0"]
    request.session["cart"] = cart
    logger.debug(cart)
    return HttpResponse(status=200, content=json.dumps(cart))
  except Exception, e:
    logger.error(e)
    return HttpResponse(status=500, content="Internal Server Failure, Check the logs!")

def add_to_cart(request):
  cart = get_cart_session(request)
  (item_id, name, size, quantity) = test_post_item(request)
  try:
    item = Item.objects.get(id=item_id)
    price = item.markdownPrice if item.markdownPrice != 0 else item.price
    desc = item.description
    image_url = item.front.url 
    existsInCart = False
    for cart_item in cart:
      if cart_item["id"] == item_id and cart_item["size"] == size:
        cart_item["quantity"] = int(cart_item["quantity"]) + int(quantity)
        existsInCart = True
    if not existsInCart:
      cart.append({"id":item_id, "price":str(price), "quantity":quantity, "size":size, "name":name, "description":desc, "image_url":image_url})
    request.session["cart"] = cart
    return HttpResponse(status=200, content=json.dumps(cart))
  except Exception, e:
    logger.error(e)
    return HttpResponse(status=500, content="Internal Server Failure, Check the logs!")

def shop_item_selected(request, item_id):
  try:
    item = Item.objects.get(id=item_id)
    size_list = item.quantity.order_by("id")
    logger.info(item)
    jsonDict = {
      "item":item.json(),
      "size_list": size_list,
      "quantity_list": range(1,11), 
      "paypal_debug" : settings.PAYPAL_DEBUG,
    }
    jsonDict.update(csrf(request))
    logger.debug(jsonDict)
    return render_to_response("website/shop_item_selected.html", jsonDict)
  except Exception, e:
    logger.error(e)
    return HttpResponseRedirect("/shop/")

def shop_guys(request):
  items = Item.objects.filter(category__parent__name="Guys", shown=True)
  sizes = Size.objects.all()
  return render_to_response("website/shop.html",
  {
    "server_url": settings.SERVER_URL,
    "item_list": items,
    "size_list": sizes,
    "paypal_debug" : settings.PAYPAL_DEBUG,
  })
def shop_girls(request):
  items = Item.objects.filter(category__parent__name="Girls", shown=True)
  sizes = Size.objects.all()
  return render_to_response("website/shop.html",
  {
    "server_url": settings.SERVER_URL,
    "item_list": items,
    "size_list": sizes,
    "paypal_debug" : settings.PAYPAL_DEBUG,
  })
def shop(request):
  gender = request.GET.get("gender",None)
  items = Item.objects.all()
  if gender:
    items = items.filter(gender=gender)
  sizes = Size.objects.all()
  return render_to_response("website/shop.html",
  {
    "server_url": settings.SERVER_URL,
    "item_list": items,
    "size_list": sizes,
    "paypal_debug" : settings.PAYPAL_DEBUG,
  })

def contact(request):
  jsonDict = {
    "paypal_debug" : settings.PAYPAL_DEBUG,
  }
  jsonDict.update(csrf(request))
  return render_to_response("website/contact.html", jsonDict)

def talent_a_m_eyes(request):
  return render_to_response("website/talent_a_m_eyes.html", {
    "paypal_debug" : settings.PAYPAL_DEBUG,
  })
def talent_cba(request):
  return render_to_response("website/talent_cba.html", {
    "paypal_debug" : settings.PAYPAL_DEBUG,
  })
def talent_mttm(request):
  return render_to_response("website/talent_mttm.html", {
    "paypal_debug" : settings.PAYPAL_DEBUG,
  })
def talent_joe_smith(request):
  return render_to_response("website/talent_joe_smith.html", {
    "paypal_debug" : settings.PAYPAL_DEBUG,
  })


def where_to_buy(request):
  return render_to_response("website/where_to_buy.html", {
    "paypal_debug" : settings.PAYPAL_DEBUG,
  })

def ttr_bs(request):
  return render_to_response("website/main_bs.html", {})

# Checkout cart

#First one:
#ON GET:

def get_tax_total(pretax_total, state="AZ"):
  """
  Charge tax where required (Use the settings file to define state tax percentages)
  """
  taxPercent = settings.PAYPAL_STATE_TAX.get(state,0)
  amountTaxed = pretax_total * taxPercent
  return (taxPercent, amountTaxed)

def get_shipping_total(cart_list):
  """
  Charge shipping based on # of cart list
  """
  if not cart_list:
    return 0.0
  item_count = len(cart_list)
  if item_count > 20:
    return 21.0
  elif item_count > 15:
    return 15.0
  elif item_count > 10:
    return 10.5
  elif item_count > 4:
    return 6.0
  elif item_count > 0:
    return 3.5

def show_cart(request):
  """
  Show the contents of the cart, include tax (9.1%) and shipping (Free!)
  When ready to continue they press button
  """
  logger.info(request)
  (cart_list, pretax_total, tax, amountTaxed, shipping_total, total) = get_cart_details(request)

  return render_to_response("website/checkout/show_cart.html", 
    {
      "cart_list" : cart_list,
      "cart_pretax" : "%.2f" % round(pretax_total,2),
      "cart_tax" : "%.1f" % round(tax*100,1),
      "cart_tax_total" : "%.2f" % round(amountTaxed,2),
      "shipping_total" : "%.2f" % round(shipping_total,2),
      "cart_total" : "%.2f" % round(total,2),
    })

#2nd page is showing the CC info and shipping info and press submit (OR paypal)
#3rd page is thank you for purchasing!
