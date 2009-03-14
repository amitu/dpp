Django PayPal Helper
====================

This application wraps PayPal API, using `django-paypal`_, and provides easy
access to do one time transfer of money. Its primary purpose is to sell
software etc.

Installation:

* Install `django-paypal`_ and configure your project accordingly
* Put dpp folder somewhere in PYTHONPATH
* Add dpp to settings.py under INSTALLED_APPS
* (r'^dpp/', include('dpp.urls')), into urls.py
* python manage.py syncdb

Usage:

* Point user to
  /dpp/start/?next=YourURL&amount=20&message=ToBeShownOnPayPalSite

It will redirect user to paypal site, and will confirm that payment has been
made. Then it will redirect users to YourURL. It stores an instance of
dpp.models.PaymentRequest in request.session["payment_request"]. Status of
payment can be obtained from PaymentRequest object.

Enjoy!

.. _`django-paypal`: http://github.com/johnboxall/django-paypal/tree/master
