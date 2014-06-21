from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^payments/', include('kid_bazaar.apps.payments.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('kid_bazaar.apps.home.urls')),
)
