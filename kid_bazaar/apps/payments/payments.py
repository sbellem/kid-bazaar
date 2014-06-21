# -*- coding: utf-8 -*-
from django.conf import settings

import braintree
import braintree.test.merchant_account as braintree_test


braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    settings.BRAINTREE_MERCHANT_ID,
    settings.BRAINTREE_PUBLIC_KEY,
    settings.BRAINTREE_PRIVATE_KEY
)


def create_submerchant(submerchant_id):
    result = braintree.MerchantAccount.create({
        'individual': {
            'first_name': braintree_test.Approve,
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
        "master_merchant_account_id": settings.BRAINTREE_MERCHANT_ACCOUNT_ID,
        "id": submerchant_id
    })
    return _format_result_create_submerchant(result)


def _format_result_create_submerchant(result_create):
    return result_create.__dict__


def do_sale(submerchant_id):
    result = braintree.Transaction.sale({
        "merchant_account_id": submerchant_id,
        "amount": "1000.00",
        "credit_card": {
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2020"
        },
        "service_fee_amount": "1.00"                                         
    })
    return _format_result_sale(result)


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
