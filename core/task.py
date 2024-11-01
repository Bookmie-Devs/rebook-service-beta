from config.sms import send_sms_message
from .models import Booking
from .models import Tenant
from celery import shared_task
from rooms_app.models import RoomProfile
from django.utils import timezone
from django.conf import settings

@shared_task()
def delete_all_expired_booking() -> None:
    """
    delete all booking that have pass the 1 hour 
    check mark
    """
    unpaid_bookings = Booking.objects.filter(end_time__lt=timezone.now())
    unpaid_bookings.delete()
    # """
    # after which rescan the room for active bookings again and
    # compare with active tenant if active booking is less
    # means booking is avaialable
    # """
    # all_rooms = RoomProfile.objects.filter(occupied=False).all()
    # for room in all_rooms:
    #     # check if room is available for booking
    #     if room.is_available_for_booking():
    #         room.booking_occupied = False
    #     # if not set booking_occupied to false
    #     else:
    #         room.booking_occupied = True

@shared_task()
def delete_all_expired_tenants() -> None:
    """
    This task deletes all tenants whoose v-code has
    expired but have not updated it after 
    """
    expired_tenants = Tenant.objects.filter(end_date__lt=timezone.now())
    expired_tenants.delete()

