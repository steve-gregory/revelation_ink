from django.contrib import admin
#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *

#from clothing.views.item import ItemManager, Item


admin.autodiscover()
def url(pattern,url,*args,**kwargs):
  return (pattern,url)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.home', name='home'),
    #url(r'^bootstrap/$', 'website.views.ttr_bs', name='bootstrap'),

    #url(r'^api/item/$', ItemManager.as_view()),
    #url(r'^api/item/(?P<item_id>.*)/$', Item.as_view()),

    url(r'^about/$', 'website.views.about', name='about'),
    url(r'^cart/complete/$', 'website.views.completeTransaction', name='Cart Purchased'),
    url(r'^cart/review/$', 'website.views.reviewTransaction', name='Purchase Cart'),
    url(r'^cart/purchase/$', 'website.views.purchase_cart', name='Purchase Cart'),
    url(r'^cart/$', 'website.views.get_cart', name='Add to cart'),
    url(r'^cart/update/$', 'website.views.update_cart', name='Add to cart'),
    url(r'^cart/add/$', 'website.views.add_to_cart', name='Add to cart'),
    url(r'^shop/(?P<item_id>.*)/$', 'website.views.shop_item_selected', name='Item selected'),
    url(r'^shop/$', 'website.views.shop', name='shop'),
    url(r'^contact/$', 'website.views.contact', name='contact'),
    url(r'^contact_form/$', 'website.views.submit_contact_form', name='contact'),
    url(r'^social/$', 'website.views.social', name='social'),
    # url(r'^revelation_ink/', include('revelation_ink.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    ### DJANGORESTFRAMEWORK ###
    #url(r'^restframework', include('djangorestframework.urls', namespace='djangorestframework'))

)
