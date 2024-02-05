from django.core.mail import EmailMessage, send_mail
from celery import shared_task

from config.sms import send_sms_message

@shared_task()
def send_email_task(subject, message, from_email, recipient_list,) -> None:
    """
    let celery send the email
    """
    email = EmailMessage(subject, message, from_email=from_email, to=recipient_list)
    email.content_subtype = "html"
    email.send(fail_silently=True)


@shared_task()
def send_sms_task(phone, msg) -> None:
    """
    let celery send the sms
    """
    send_sms_message(user_contact=phone, msg=msg)

@shared_task()
def test_function():
    from core.models import Booking
    from django.utils import timezone
    unpaid_bookings = Booking.objects.filter(end_time__lt=timezone.now())
    unpaid_bookings.delete()