from django.conf.urls import patterns, url

from .views import sale, submerchant


urlpatterns = patterns('',
    url(r'^sale/(?P<item_id>\d+)', sale),
    url(r'^submerchant/', submerchant),
)
