from django.conf.urls import patterns, url

from .views import pay, create


urlpatterns = patterns('',
    url(r'^pay/', pay),
    url(r'^create/', create),
)
