from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^ipn/$', 'paypal.standard.views.ipn'),
    url(r'^return/$', 'dpp.views.return_'),
    url(r'^start/$', 'dpp.views.start'),
)
