import requests
from django.conf import settings



heeaders = {
    "Authorization" : f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    "Content-Type" : "application/json",
}

def paystack_verification(reference):

    paystack_url = f"https://api.paystack.co/transaction/verify/{reference}"

    response = requests.get(url=paystack_url,headers=heeaders,)

    return response

def create_subaccount(hostel=None):

    paystack_url = 'https://api.paystack.co/subaccount'

    data = {
        "business_name": str(hostel.hostel_name).upper(), 
        "bank_code": hostel.bank_code, 
        "account_number": hostel.account_number, 
        "percentage_charge": 0.95 
    }

    response = requests.post(url=paystack_url,headers=heeaders, data=data)

    return response

def redirect_payment(customer=None, room=None, hostel=None):
    
    paystack_url = 'https://api.paystack.co/transaction/initialize'

    data = {
        "email": customer.email, 
        "amount": room.romm_price, 
        "subaccount": hostel.sub_account_code
    }

    response = requests.post(url=paystack_url,headers=heeaders, data=data)

    return response