from django.conf.urls import url
from marketing.sitemap import SITEMAPS
from django.contrib.sitemaps.views import sitemap
from .views import robots


urlpatterns = [
    url(r'^robots\.txt$', robots, name='robots'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': SITEMAPS}, name='sitemap'),
]
