# imports # {{{
from django.db import models

from datetime import datetime
from paypal.standard.models import PayPalIPN
# }}}

# PaymentStatusChoices # {{{ 
PaymentStatusChoices = (
    ('P','Processing'),
    ('S','Success'),
    ('F','Failed'),
)
# }}} 

# PaymentRequest # {{{ 
class PaymentRequest(models.Model):
    # flow: # {{{ 
    #   1) Psuedo buttons with amount are created, when they are clicked
    #   2) /start/1/ url is called, which enters data in model with "status" set to "processing" 
    #      Actual Buttons are rendered using PayPalPaymentsForm and submit is called on html onload()
    #   3) The /return/1/ url shows "processing" and refreshes itself periodically
    #   4) Paypal calls ipn, on success signal, "status" is changed to "SUCCESS" or "FAILED" for 3) to
    #       get current "status"
    ## TODO: Add requested amount, given amount, status-of-proper-transaction ()
    ## if selected denomination is not 2,5,10,50  go back to main page
    ## use click button, and onload html takes it to paypal,
    ## success page to have GIFT CERTIFICATE and PHONE NUMBER choice
    ## take phone number from session
    ## 4 buttons for Gift Certification and 4 for crediting mobile 
    ## use custom field to store session-phone session-mailid
    # }}} 
    session_data = models.TextField()
    status = models.CharField(max_length=10, choices=PaymentStatusChoices)
    next = models.CharField(max_length=200)
    cancel = models.CharField(max_length=200)
    requested_amount = models.FloatField()
    message = models.CharField(max_length=100)

    # Payment Gateway return values
    pg_transferred_amount = models.FloatField(blank=True, null=True)
    pg_payment_status = models.CharField(max_length=20, blank=True)
    pg_currency_code = models.CharField(max_length=30, blank=True)
    pg_custom = models.CharField(max_length=100, blank=True)
    pg_ipn_on = models.DateTimeField(null=True, blank=True)

    paypal_ipn = models.ForeignKey(PayPalIPN, null=True, blank=True)

    created_on = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return "%s, $%s, %s" % (
            self.message, self.requested_amount, self.get_status_display()
        )
# }}} 

import dpp.signals
