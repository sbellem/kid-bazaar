from django.conf.urls import include, patterns, url

from .views import passed, cancelled, sale


urlpatterns = patterns('',
    url(r'^sale/(?P<item_id>\d+)', sale, name='do_sale'),
    url(r'^passed/', passed),
    url(r'^cancelled/', cancelled),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
)
