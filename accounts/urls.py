from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'my_account/$', views.my_account, name='my_account'),
    url(r'^order_details/(?P<order_id>[-\w]+)/$', views.order_details, name='order_details'),
    url(r'^order_info/$', views.order_info, name='order_info'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout')
]