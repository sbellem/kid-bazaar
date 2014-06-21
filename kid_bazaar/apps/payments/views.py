# -*- coding: utf-8 -*-
from django.shortcuts import render

from .payments import do_sale, create_submerchant


def pay(request):
    if request.method == 'GET':
        return render(request, 'payments/pay.html')

    sale_result = do_sale(request.POST.get('user_id'))
    return render(request, 'payments/pay.html', {
        'result': sale_result
    })


def create(request):
    if request.method == 'GET':
        return render(request, 'payments/create.html')

    create_result = create_submerchant(request.POST.get('user_id'))
    return render(request, 'payments/create.html', {
        'result': create_result
    })
    