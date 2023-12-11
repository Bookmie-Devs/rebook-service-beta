from .models import Booking
from rooms_app.models import RoomProfile
from django.utils import timezone


def delete_all_expired_booking() -> None:
    """
    delete all booking that have pass the 1 hour 
    check mark
    """
    unpaid_bookings = Booking.objects.filter(end_time__lt=timezone.now())
    unpaid_bookings.delete()
    """
    after which rescan the room for active bookings again and
    compare with active tenant if active booking is less
    means booking is avaialable
    """
    all_rooms = RoomProfile.objects.filter(occupied=False).all()
    for room in all_rooms:
        if room.active_bookings()<room.active_tenants():
            room.booking_occupied = False
        else:
            room.booking_occupied = True
   