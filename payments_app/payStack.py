import requests
from django.conf import settings
from hostel_app.models import HostelProfile
from django.urls import reverse

headers = {
    "Authorization" : f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    "Content-Type" : "application/json",
}


def create_subaccount(hostel: HostelProfile=None):

    paystack_url = 'https://api.paystack.co/subaccount'

    data = {
        "business_name": str(hostel.hostel_name).upper(), 
        "bank_code": str(hostel.bank_code), 
        "account_number": str(hostel.account_number), 
    
        "primary_contact_name":str(hostel.hostel_contact),

        #the percenetage charge for every hostel sub account
        "percentage_charge": settings.SUBACCOUNT_PERCENTAGE, ############################
    }
    response = requests.post(url=paystack_url,headers=headers,json=data)
    
    return response


def paystack_verification(reference):
    # url for checking reference
    paystack_url = f"https://api.paystack.co/transaction/verify/{reference}"

    response = requests.get(url=paystack_url,headers=headers,)
    return response

# confirm payment dat from paystack
def payment_is_confirm(data, amount):
    if (data.status_code==200 and 
        data.json()['data'].get('status')=="success" and
        data.json()['data'].get('amount')==amount*100):
        return True
    else:
        return False
    

def update_subaccount(subaccount_id, hostel_name, settlement_bank, account_number, percentage_charge):
    paystack_url = f'https://api.paystack.co/subaccount/{subaccount_id}'
    data = {
    'business_name':f'{hostel_name}',
    'settlement_bank':f'{settlement_bank}',
    'account_number': f'{account_number}',
    'percentage_charge':f'{percentage_charge}',
    }
    response = requests.put(url=paystack_url, json=data, headers=headers)
    print(response.json())
    if response.status_code==200 and response.json().get('status')==True:
        return response.json().get('message')
    else:
        return "Error Occured"
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