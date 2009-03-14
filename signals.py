# imports # {{{ 
from paypal.standard.signals import payment_was_successful
from paypal.standard.signals import payment_was_flagged

import datetime

from dpp.models import PaymentRequest
# }}} 

# update_status_success # {{{ 
def update_status_success(sender, **kwargs):
    ipn_obj = sender
    ipn_obj.save()
    invoiceid = ipn_obj.invoice
    paydata = PaymentRequest.objects.get(id=invoiceid)
    paydata.status = 'S'
    paydata.pg_transferred_amount = float(ipn_obj.mc_gross)
    paydata.pg_payment_status = ipn_obj.payment_status
    paydata.pg_currency_code = ipn_obj.mc_currency
    paydata.pg_custom = ipn_obj.custom
    paydata.pg_ipn_on = datetime.datetime.now()
    paydata.paypal_ipn = ipn_obj 
    paydata.save() 

payment_was_successful.connect(update_status_success)
# }}} 

# update_status_flagged # {{{ 
def update_status_flagged(sender, **kwargs):
    ipn_obj = sender
    ipn_obj.save()
    invoice = ipn_obj.invoice
    paydata = PaymentRequest.objects.get(id=invoice)
    paydata.status = 'F' 
    paydata.pg_ipn_on = datetime.datetime.now()
    paydata.paypal_ipn = ipn_obj
    paydata.save() 

payment_was_flagged.connect(update_status_flagged)
# }}} 
