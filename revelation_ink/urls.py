from django.contrib import admin
#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from website.api import ContactForm
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

    #User sees the cart, can start the checkout purchase
    url(r'^cart/show/$', 'website.views.show_cart', name='Show Cart'),
    #User gives information
    url(r'^checkout/collect/$', 'website.views.collect_billing_info', name='Collect card info'),
    #User reviews information (POST ONLY)
    url(r'^checkout/review/$', 'website.views.reviewTransaction', name='Cart Purchased'),
    #User completed CC info
    url(r'^checkout/complete$', 'website.views.purchase_complete', name='Checkout Completed'),

    url(r'^cart/$', 'website.views.get_cart', name='Add to cart'),
    url(r'^cart/update/$', 'website.views.update_cart', name='Add to cart'),
    url(r'^cart/add/$', 'website.views.add_to_cart', name='Add to cart'),


    url(r'^shop/guys/$', 'website.views.shop_guys', name='shop guys'),
    url(r'^shop/girls/$', 'website.views.shop_girls', name='shop girls'),
    url(r'^shop/$', 'website.views.shop', name='shop'),
    url(r'^shop/(?P<item_id>.*)/$', 'website.views.shop_item_selected', name='Item selected'),
    url(r'^contact/$', 'website.views.contact', name='contact'),
    url(r'^contact_form/$', ContactForm.as_view(), name='contact'),
    url(r'^where_to_buy/$', 'website.views.where_to_buy', name='where_to_buy'),
    url(r'^talent/a_m_eyes/$', 'website.views.talent_a_m_eyes', name='talent_ameyes'),
    url(r'^talent/joe_smith/$', 'website.views.talent_joe_smith', name='talent_joe_smith'),
    url(r'^talent/cba/$', 'website.views.talent_cba', name='talent_cba'),
    url(r'^talent/mttm/$', 'website.views.talent_mttm', name='talent_mttm'),
    # url(r'^revelation_ink/', include('revelation_ink.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    ### DJANGORESTFRAMEWORK ###
    #url(r'^restframework', include('djangorestframework.urls', namespace='djangorestframework'))

)
