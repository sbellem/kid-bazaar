from django.conf.urls import patterns, url

from .views import pay 


urlpatterns = patterns('',
    url(r'^pay/', pay),
)
