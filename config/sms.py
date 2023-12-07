from django.conf import settings
import requests

api_key = settings.SMS_API_KEY

sender_id = settings.SENDER_ID

endpoint = "https://apps.mnotify.net/smsapi"

def send_sms_message(user_contact=None, msg=None):
    # print(user_contact)
    # print(sender_id)
    params = {
        "key":api_key,
        "to": user_contact,
        "msg": msg,
        "sender_id" : settings.SENDER_ID,
    }
    if settings.DEBUG:
       pass
    else:
        requests.post(url=endpoint, params=params)

    # print(requests.post(url=endpoint, params=params).json())
    