import braintree
from django.conf import settings
from django.shortcuts import render


def test_pay():
    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        settings.BRAINTREE_MERCHANT_ID,
        settings.BRAINTREE_PUBLIC_KEY,
        settings.BRAINTREE_PRIVATE_KEY
    )
    result = braintree.Transaction.sale({
        "amount": "1000.00",
        "credit_card": {
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2020"
        }
    })
    return result
    
        
def pay(request):
    payment_result = test_pay()

    payment_result_details = ''
    if payment_result.is_success:
        payment_result_details += "\nsuccess!: " + payment_result.transaction.id
    elif payment_result.transaction:
        payment_result_details += "\nError processing transaction:"
        payment_result_details += "\n  message: " + payment_result.message
        payment_result_details += "\n  code:    " + payment_result.transaction.processor_response_code
        payment_result_details += "\n  text:    " + payment_result.transaction.processor_response_text
    else:
        payment_result_details += "\nmessage: " + payment_result.message
        for error in payment_result.errors.deep_errors:
            payment_result_details += "\nattribute: " + error.attribute
            payment_result_details += "\n  code: " + error.code
            payment_result_details += "\n  message: " + error.message

    return render(request, 'payments/pay.html', {'payment_result_details': payment_result_details})
