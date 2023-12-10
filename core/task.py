from .models import Booking
from django.utils import timezone


def delete_all_expired_booking():
    """
    delete all booking that have pass the 1 hour 
    check mark
    """
    all_booking = Booking.objects.filter(end_time__lt=timezone.now())
    all_booking.delete()
