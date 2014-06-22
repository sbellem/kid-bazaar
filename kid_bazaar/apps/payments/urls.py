from django.conf.urls import patterns, url

from .views import sale


urlpatterns = patterns('',
    url(r'^sale/(?P<item_id>\d+)', sale, name='do_sale'),
)
