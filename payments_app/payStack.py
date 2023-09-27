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
