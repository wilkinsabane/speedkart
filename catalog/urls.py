from django.conf.urls import url
from catalog import views


urlpatterns = [
    url(r'^$', views.index, name='catalog_home'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', views.show_category, name='catalog_category'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', views.show_product, name='catalog_product'),
    url(r'^review/product/add/$', views.add_review, name='add_review')
]