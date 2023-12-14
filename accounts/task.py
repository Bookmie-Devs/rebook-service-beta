from django.core.mail import send_mail
from celery import shared_task

from config.sms import send_sms_message

@shared_task()
def send_email_task(from_email, recipient_list, subject, message,) -> None:
    """
    let celery send the email
    """
    send_mail(from_email=from_email, recipient_list=recipient_list, subject=subject, message=message,
              fail_silently=True)


@shared_task()
def send_sms_task(phone, msg) -> None:
    """
    let celery send the sms
    """
    send_sms_message(user_contact=phone, msg=msg)

@shared_task()
def test_function():
    from time import sleep
    sleep(32)