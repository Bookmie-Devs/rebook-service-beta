import requests
from django.conf import settings
from hostel_app.models import HostelProfile
from .models import PaystackSubAccount
from django.urls import reverse

headers = {
    "Authorization" : f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    "Content-Type" : "application/json",
}

def paystack_verification(reference):
    
    # url for checking reference
    paystack_url = f"https://api.paystack.co/transaction/verify/{reference}"

    response = requests.get(url=paystack_url,headers=headers,)
    return response

def create_subaccount(hostel=None):

    paystack_url = 'https://api.paystack.co/subaccount'

    data = {
        "business_name": str(hostel.hostel_name).upper(), 
        "bank_code": str(hostel.bank_code), 
        "account_number": str(hostel.account_number), 
    
        "primary_contact_name":str(hostel.contact),

        #the percenetage charge for every hostel sub account
        "percentage_charge": 0.95, ############################
    }


    response = requests.post(url=paystack_url,headers=headers,json=data)
    
    return response


# def redirect_payment(customer_email=None, reference=None, room_price=None, hostel=None):

#     #   get hostel sub account
#     hostel_sub_account = PaystackSubAccount.objects.get(hostel=hostel)

#     # paystack transaction endpoint
#     paystack_url = 'https://api.paystack.co/transaction/initialize'

#     #data for redirecting
#     data = {
#         "email": customer_email, 
#         # change decimal value to float
#         "amount": float(room_price), # to make it json seriable

#         # call back url when payment is completed"""
#         # change domain in production
#         "callback_url":"https://ethenatx.pythonanywhere.com/payments/verify-payment/",

#         # refernce
#         "reference": reference,

#         "subaccount": hostel_sub_account.subaccount_code
#     }

#     response = requests.post(url=paystack_url,headers=headers, json=data)
#     return response