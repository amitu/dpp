# imports # {{{ 
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from paypal.standard.forms import PayPalPaymentsForm
from pprint import pformat 

from dpp.models import PaymentRequest
# }}} 

# start # {{{ 
def start(request):
    next = request.GET['next']
    requested_amount = request.GET['amount']
    message = request.GET['message']
    cancel = request.GET.get('cancel', next)
    session_data = pformat(request.session)
    payment_request = PaymentRequest.objects.create(
        status='P', next=next, cancel=cancel,
        requested_amount=requested_amount, message=message,
        session_data = session_data,
    ) 
    logger.info("Created PaymentRequest, %s" % payment_request.id) 
    form = PayPalPaymentsForm(
        initial = {
            "business": "exampl@amitu.com",
            "item_name": "Example Store:" + message,
            "amount": requested_amount,
            "invoice": payment_request.id,
            "notify_url": "http://www.example.com/dpp/ipn/?id=%s" % (
                payment_request.id
            ),
            "return_url": "http://www.example.com/dpp/return/?id=%s" % (
                payment_request.id
            ),
            "cancel_return": (
                "http://www.example.com/dpp/return/?cancel=true&id=%s" % (
                    payment_request.id
                )
            )
        }
    )
    return render_to_response(
        "dpp/start.html", {'form': form}, 
        context_instance=RequestContext(request),
    )
# }}}  

# return # {{{ 
def return_(request):
    if "check" not in request.REQUEST:
        id = request.GET['id']
        payment_request = PaymentRequest.objects.get(id=id)
        request.session['payment_request'] = payment_request
        return HttpResponseRedirect("%s?check=true" % request.path)
    request.session['payment_request'] = PaymentRequest.objects.get(
        id=request.session['payment_request'].id
    )
    return render_to_response(
        "dpp/return.html", {'session': request.session},
        context_instance = RequestContext(request),
	)
# }}} 
