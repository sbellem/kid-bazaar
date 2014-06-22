# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm

from kid_bazaar.apps.home.models import Item 

from .payments import do_sale



def view_that_asks_for_money(request):

    # What you want the button to do.
    # Create the instance.
    context = {"form": form}
    return render_to_response("payment.html", context)


def passed(request):
    messages.add_message(request, messages.SUCCESS, 'Payment received')
    return redirect(reverse('my_items'))


def cancelled(request):
    messages.add_message(request, messages.SUCCESS, 'Payment cancelled')
    return redirect(reverse('my_items'))


def sale(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    #import ipdb; ipdb.set_trace()
    paypal_dict = {
        "business": item.owner.parent.email,
        "amount": item.price,
        "item_name": item.name,
        "invoice": "unique-invoice-id",
        "notify_url": "https://kidsbazaar.cloudcontrol.com" + reverse('paypal-ipn'),
        "return_url": "https://kidsbazaar.cloudcontrolapp.com/payments/passed/",
        "cancel_return": "https://kidsbazaar.cloudcontrolapp.com/payments/cancelled/",
    }
    form = PayPalPaymentsForm(initial=paypal_dict)

    ctx = {
        'item': item,
        'form': form
    } 

    if request.method == 'GET':
        return render(request, 'payments/pay.html', ctx)
    
    ctx['result'] = do_sale(
        item.owner.parent.merchant_id, 
        request.POST.get('cc_number'),
        request.POST.get('cc_expires_month'),
        request.POST.get('cc_expires_year'),
        item.id,
        item.price
    )
    item.update_is_paid()
    return HttpResponseRedirect(reverse('my_items'))
    