# -*- coding: utf-8 -*-
import braintree
from django.conf import settings
from django.shortcuts import render


braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    settings.BRAINTREE_MERCHANT_ID,
    settings.BRAINTREE_PUBLIC_KEY,
    settings.BRAINTREE_PRIVATE_KEY
)


def _test_merchantaccount_create():
    return braintree.MerchantAccount.create({
        'individual': {
            'first_name': "Jane",
            'last_name': "Doe",
            'email': "jane@14ladders.com",
            'phone': "5553334444",
            'date_of_birth': "1981-11-19",
            'ssn': "456-45-4567",
            'address': {
                'street_address': "111 Main St",
                'locality': "Chicago",
                'region': "IL",
                'postal_code': "60622"
            }
        },
        'business': {
            'legal_name': "Jane's Ladders",
            'dba_name': "Jane's Ladders",
            'tax_id': "98-7654321",
            'address': {
                'street_address': "111 Main St",
                'locality': "Chicago",
                'region': "IL",
                'postal_code': "60622"
            }
        },
        'funding': {
            'destination': braintree.MerchantAccount.FundingDestination.Bank,
            'email': "funding@blueladders.com",
            'mobile_phone': "5555555555",
            'account_number': "1123581321",
            'routing_number': "071101307",
        },
        "tos_accepted": True,
        "master_merchant_account_id": settings.BRAINTREE_MERCHANT_ID,
        "id": "blue_ladders_store"
    })


def _test_transaction_sale():
    result = braintree.Transaction.sale({
        "amount": "1000.00",
        "credit_card": {
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2020"
        }
    })
    return result


def _format_result_sale(result_sale):
    result_sale_details = ''
    if result_sale.is_success:
        result_sale_details += "\nsuccess!: " + result_sale.transaction.id
    elif result_sale.transaction:
        result_sale_details += "\nError processing transaction:"
        result_sale_details += "\n  message: " + result_sale.message
        result_sale_details += "\n  code:    " + result_sale.transaction.processor_response_code
        result_sale_details += "\n  text:    " + result_sale.transaction.processor_response_text
    else:
        result_sale_details += "\nmessage: " + result_sale.message
        for error in result_sale.errors.deep_errors:
            result_sale_details += "\nattribute: " + error.attribute
            result_sale_details += "\n  code: " + error.code
            result_sale_details += "\n  message: " + error.message
    return result_sale_details


def pay(request):
    result_sale = _test_transaction_sale()
    return render(request, 'payments/pay.html', {
        'result': _format_result_sale(result_sale)
    })


def create(request):
    result_create = _test_merchantaccount_create()
    return render(request, 'payments/create.html', {
        'result': result_create.message
    })
