from django.db import models
import os
# Create your models here.
class Size(models.Model):
  """
    Known Sizes:
    'One-Size'
    'Small'
    'Medium'
    'Large'
    'X-Large'
    'Small/Medium'
    'Large/X-Large'
  """
  name = models.CharField(max_length=128)

  def __unicode__(self):
    return "%s" % (self.name,)
  
class Category(models.Model):
  """
  Sample category: Pants, Shirt, Hat, Sticker
  """
  #TODO: Force validation of two parent maximum?
  name = models.CharField(max_length=128)
  parent = models.ForeignKey('Category', blank=True, null=True) # Points to parent, creates inherit tree

  def __unicode__(self):
    return "%s%s" % ( self.name,"" if not self.parent else " (%s)" % (self.parent.name,) )


def featured_image(self, filename):
  ext = filename.split('.')[-1]
  #Validate extension
  filename = '%s%s.%s' % (self.name,'_featured',ext)
  return os.path.join('uploads/clothes', filename)

def front_image(self, filename):
  ext = filename.split('.')[-1]
  #Validate extension
  filename = '%s%s.%s' % (self.name,'_front',ext)
  return os.path.join('uploads/clothes', filename)

def back_image(self, filename):
  ext = filename.split('.')[-1]
  #Validate extension
  filename = '%s%s.%s' % (self.name,'_back',ext)
  return os.path.join('uploads/clothes', filename)

class Item(models.Model):
  """
  @name - Name of the item (White T)
  @category - category of item (Shirt)
  @desc - Describe the item (It's white..)
  @sizes - Available sizes for item (S,M,L,XL)
  @sku - SKU for item (01234567)
  @price - ORIGINAL price of the item ($30.00)
  @markdown price - ACTUAL price of the item ($20.00)
  @featured - Show the item on the home page
  @shown - Show the image on the shop page
  @front - Front/First picture of item
  @back - Back/Second picture of item
  """
  
  name = models.CharField(max_length=128)
  category = models.ForeignKey(Category)
  description = models.TextField()
  quantity = models.ManyToManyField(Size, through='Stock')
  sku = models.CharField(max_length=255, default='')
  price = models.DecimalField(max_digits=5, decimal_places=2, default=0)# Max value is 999.00
  markdownPrice = models.DecimalField(max_digits=5, decimal_places=2, default=0) # Make it easy to 'mark-down' clothes and have it show up on website
  featured = models.BooleanField(default=False) #Should this clothing item be featured (on the home page?)
  shown = models.BooleanField(default=True) #Should this clothing item be shown in the shop?

  featured_image = models.ImageField(upload_to=featured_image, blank=True, null=True)
  front = models.ImageField(upload_to=front_image, blank=True, null=True)
  back = models.ImageField(upload_to=back_image, blank=True, null=True)

  def __unicode__(self):
    return "%s <%s> - $%s" % (self.name, self.category, self.markdownPrice)

  def json(self):
    return {
      'id':self.id,
      'name':self.name,
      'price':self.price,
      'markdownPrice':self.markdownPrice,
      'front_url':self.front.url if self.front else '',
      'back_url':self.back.url if self.back else '',
      #Change to list: [pictures] in order
      'description':self.description,
      'sku':self.sku,
    }

class Stock(models.Model):
  """
  Items have a specified quantity of size:
  T-shirt has 5 XL, 10 L, 10 Sm..
  -1 = Unlimited Quantity
  This must be updated by danny
  """
  item = models.ForeignKey(Item)
  size = models.ForeignKey(Size)
  quantity = models.IntegerField(default=-1)

  def __unicode__(self):
    return "%s - $%s" % (self.item, self.size)

class StockSold(models.Model):
  item = models.ForeignKey(Item)
  size = models.ForeignKey(Size)
  count = models.IntegerField(default=1)

  def __unicode__(self):
    return "%s %s(%s) Size:%s" % (self.count, self.item.name,self.item.sku, self.size)


class Transaction(models.Model):
  items_sold = models.ManyToManyField(StockSold, blank=True, null=True)
  full_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  shipping_info = models.TextField()
  billing_info = models.TextField()
  confirmation_id = models.CharField(max_length=255)
  shipped = models.BooleanField(default=False)
  def __unicode__(self):
    return "%s for: %s Shipped:%s" % (self.items_sold.all(), self.full_name,self.shipped)
