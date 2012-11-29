from django.db import models

from django.db import models
import os
# Create your models here.

class AboutPagePhoto(models.Model):
  """
  The about page photos can be uploaded here, and will be shown in weight-then-id order
  Increase weight to make the photo show up later
  """
  name = models.CharField(max_length=128)
  weight = models.IntegerField(default=0)
  image = models.ImageField(upload_to='website/about_page_photos')
  visible = models.BooleanField(default=True)

  def __unicode__(self):
    return "%s <%s>" % (self.name,self.image)

class FrontPagePhoto(models.Model):
  """
  The front page photos can be uploaded here, and will be shown in weight-then-id order
  Increase weight to make the photo show up later
  """
  name = models.CharField(max_length=128)
  weight = models.IntegerField(default=0)
  image = models.ImageField(upload_to='website/front_page_photos')
  visible = models.BooleanField(default=True)

  def __unicode__(self):
    return "%s <%s>" % (self.name,self.image)
