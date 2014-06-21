from django.shortcuts import render


def pay(request):
    return render(request, 'payments/pay.html', {}, content_type="application/xhtml+xml")    