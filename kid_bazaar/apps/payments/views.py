# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from kid_bazaar.apps.home.models import Item 

from .payments import do_sale


def sale(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    ctx = {
        'item': item
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
    return render(request, 'payments/pay.html', ctx)
    