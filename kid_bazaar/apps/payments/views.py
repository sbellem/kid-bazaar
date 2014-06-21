# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from kid_bazaar.apps.home.models import Item 

from .payments import do_sale, create_submerchant


def sale(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    ctx = {
        'item': item
    } 

    if request.method == 'GET':
        return render(request, 'payments/pay.html', ctx)

    sale_result = do_sale(item.owner.parent.merchant_id, item.price)
    ctx['result'] = sale_result
    return render(request, 'payments/pay.html', ctx)


def submerchant(request):
    if request.method == 'GET':
        return render(request, 'payments/create.html')

    create_result = create_submerchant(request.POST.get('user_id'))
    return render(request, 'payments/create.html', {
        'result': create_result
    })
    