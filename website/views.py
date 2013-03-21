from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from paypal.driver import PayPal
from revelation_ink import settings
from revelation_ink.logger import logger
from clothing.models import Item, Size, StockSold, Transaction
from website.models import AboutPagePhoto, FrontPagePhoto
try:
  import json
except:
  import simplejson as json
def backbone_ex(request):
  return render_to_response('backbone/index.html', {})

def home(request):
  photos = FrontPagePhoto.objects.order_by('weight')
  image_list = [p.image.url for p in photos] 
  logger.debug(image_list)
  return render_to_response('website/index.html', 
    {
      'image_list' : image_list,
      'paypal_debug' : settings.PAYPAL_DEBUG,
    })

def about(request):
  photos = AboutPagePhoto.objects.order_by('weight')
  image_list = [p.image for p in photos] 
  return render_to_response('website/about.html', 
    {
      'image_list' : image_list,
      'paypal_debug' : settings.PAYPAL_DEBUG,
    })

def get_cart(request):
  cart = request.session.get('cart',[])
  return HttpResponse(content=json.dumps(cart))

def get_cart_session(request):
  try:
    #Return cart OR an empty list
    return request.session.get('cart',[])
  except Exception, e:
    logger.error("Session failure")
    logger.error(e)
    return HttpResponse(status=500, content='Internal Server Failure')

def test_post_item(request):
  try:
    #Add the new item to cart
    item_id = request.POST['id']
    name = request.POST['name']
    size = request.POST['size']
    quantity = request.POST['quantity']
    return (item_id, name, size, quantity)
  except Exception, e:
    logger.error(e)
    return HttpResponse(status=400, content='Bad params passed, expects id, name, size & quantity')

def purchase_cart(request):
  logger.info(request)
  cart = get_cart_session(request)
  cartTotal = 0
  for cart_item in cart:
    item = Item.objects.get(id=cart_item['id'])
    itemPrice = item.markdownPrice if item.markdownPrice else item.price
    itemTotal = int(cart_item['quantity']) * itemPrice
    cartTotal = cartTotal + itemTotal
  p = PayPal()
  p.SetExpressCheckout("%.2f" % round(cartTotal,2), 'USD', settings.SERVER_URL+'cart/review/', settings.SERVER_URL, NOSHIPPING=0)
  request.session['paypal_total'] = cartTotal
  request.session['paypal_token'] = p.token
  return HttpResponseRedirect(p.paypal_url())

def getCartList(request):
  cart_list = []
  cart = get_cart_session(request)
  cartTotal = 0
  for cart_item in cart:
    item = Item.objects.get(id=cart_item['id'])
    itemPrice = item.markdownPrice if item.markdownPrice else item.price
    total = itemPrice * int(cart_item['quantity'])
    cartTotal = cartTotal + total
    cart_list.append({
	'id': cart_item['id'],
	'size': cart_item['size'],
	'image_url': item.front.url,
	'total': '%.2f' % round(total,2),
	'quantity': cart_item['quantity'],
	'description': item.description,
	})
  return (cart_list,cartTotal)

def reviewTransaction(request):
  logger.info(request)
  (cart_list,cartTotal) = getCartList(request)
  request.session['paypal_PayerID'] = request.GET['PayerID']
  request.session['paypal_token'] = request.GET['token']
  return render_to_response('website/review_transaction.html', 
    {
      'cart_list' : cart_list,
      'cart_total' : '%.2f' % round(cartTotal,2),
      'paypal_debug' : settings.PAYPAL_DEBUG,
    })
  #Show modal dialog on its own screen
  #On "OKAY" click 'DoExpressCheckoutPayment'

def completeTransaction(request):
  logger.info(request)
  #Clear the cart
  (cart_list,cartTotal) = getCartList(request)
  p = PayPal()
  cartTotal = request.session['paypal_total']
  p.DoExpressCheckoutPayment("USD", "%.2f" % round(cartTotal,2), request.session['paypal_token'], request.session['paypal_PayerID'])
  #Test 'status == ok'
  #Create a new transaction
  p.GetExpressCheckoutDetails(settings.SERVER_URL+'cart/review/', settings.SERVER_URL, request.session['paypal_token'])
  name = '%s %s' % (p.api_response['FIRSTNAME'],p.api_response['LASTNAME'])
  email = p.api_response['EMAIL']
  #'Address\n\nTucson,AZ 85704'
  address = '%s\n%s\n%s,%s %s' % (p.api_response.get('SHIPTOSTREET','No Street Info'), p.api_response.get('SHIPTOSTREET2',''), p.api_response.get('SHIPTOCITY','No City'), p.api_response.get('SHIPTOSTATE','NoState'), p.api_response.get('SHIPTOZIP','No ZIP'))
  #Remove the cart and paypal variables
  transaction = Transaction(full_name=name, email=email, shipping_info=address)
  transaction.save()
  for list_item in cart_list:
    item = Item.objects.get(id=list_item['id'])
    size = Size.objects.get(name=list_item['size'])
    sold_item = StockSold(item=item, size=size, count=list_item['quantity'])
    sold_item.save()
    transaction.items_sold.add(sold_item)
  #transaction.save()
  del request.session['cart'] 
  del request.session['paypal_PayerID'] 
  del request.session['paypal_token'] 
  return render_to_response('website/thank_you_transaction.html',
	{
	  'cart_list' : cart_list,
	  'cart_total' : '%.2f' % round(cartTotal,2),
    'paypal_debug' : settings.PAYPAL_DEBUG,
	})

def update_cart(request):
  cart = get_cart_session(request)
  (item_id, name, size, quantity) = test_post_item(request)
  try:
    item = Item.objects.get(id=item_id)
    logger.debug(cart)
    for cart_item in cart:
      #If item in cart matches ID and size
      if cart_item['id'] == item_id and cart_item['size'] == size:
        cart_item['quantity'] = quantity
    cart = [item for item in cart if item['quantity'] != '0']
    request.session['cart'] = cart
    logger.debug(cart)
    return HttpResponse(status=200, content=json.dumps(cart))
  except Exception, e:
    logger.error(e)
    return HttpResponse(status=500, content='Internal Server Failure, Check the logs!')

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
      if cart_item['id'] == item_id and cart_item['size'] == size:
        cart_item['quantity'] = int(cart_item['quantity']) + int(quantity)
        existsInCart = True
    if not existsInCart:
      cart.append({'id':item_id, 'price':str(price), 'quantity':quantity, 'size':size, 'name':name, 'description':desc, 'image_url':image_url})
    request.session['cart'] = cart
    return HttpResponse(status=200, content=json.dumps(cart))
  except Exception, e:
    logger.error(e)
    return HttpResponse(status=500, content='Internal Server Failure, Check the logs!')

def shop_item_selected(request, item_id):
  try:
    item = Item.objects.get(id=item_id)
    size_list = item.quantity.order_by('id')
    logger.info(item)
    jsonDict = {
      'item':item.json(),
      'size_list': size_list,
      'quantity_list': range(1,11), 
      'paypal_debug' : settings.PAYPAL_DEBUG,
    }
    jsonDict.update(csrf(request))
    logger.debug(jsonDict)
    return render_to_response('website/shop_item_selected.html', jsonDict)
  except Exception, e:
    logger.error(e)
    return HttpResponseRedirect('/shop/')

def shop_guys(request):
  items = Item.objects.filter(category__parent__name='Guys')
  sizes = Size.objects.all()
  return render_to_response('website/shop.html',
  {
    'item_list': items,
    'size_list': sizes,
    'paypal_debug' : settings.PAYPAL_DEBUG,
  })
def shop_girls(request):
  items = Item.objects.filter(category__parent__name='Girls')
  sizes = Size.objects.all()
  return render_to_response('website/shop.html',
  {
    'item_list': items,
    'size_list': sizes,
    'paypal_debug' : settings.PAYPAL_DEBUG,
  })
def shop(request):
  gender = request.GET.get('gender',None)
  items = Item.objects.all()
  if gender:
    items = items.filter(gender=gender)
  sizes = Size.objects.all()
  return render_to_response('website/shop.html',
  {
    'item_list': items,
    'size_list': sizes,
    'paypal_debug' : settings.PAYPAL_DEBUG,
  })

def contact(request):
  jsonDict = {
    'paypal_debug' : settings.PAYPAL_DEBUG,
  }
  jsonDict.update(csrf(request))
  return render_to_response('website/contact.html', jsonDict)

def talent_a_m_eyes(request):
  return render_to_response('website/talent_a_m_eyes.html', {
    'paypal_debug' : settings.PAYPAL_DEBUG,
  })
def talent_cba(request):
  return render_to_response('website/talent_cba.html', {
    'paypal_debug' : settings.PAYPAL_DEBUG,
  })
def talent_mttm(request):
  return render_to_response('website/talent_mttm.html', {
    'paypal_debug' : settings.PAYPAL_DEBUG,
  })
def talent_joe_smith(request):
  return render_to_response('website/talent_joe_smith.html', {
    'paypal_debug' : settings.PAYPAL_DEBUG,
  })


def where_to_buy(request):
  return render_to_response('website/where_to_buy.html', {
    'paypal_debug' : settings.PAYPAL_DEBUG,
  })

def ttr_bs(request):
  return render_to_response('website/main_bs.html', {
    'paypal_debug' : settings.PAYPAL_DEBUG,
  })
