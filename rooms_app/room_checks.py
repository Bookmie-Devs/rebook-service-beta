"""
room check logics and functions here to avoid
circular import errors with importing
classes
"""
from campus_app.models import CampusProfile
from core.models import Booking, Tenant
from rooms_app.models import RoomProfile
from django.utils import timezone

def active_bookings(room_instance: RoomProfile) -> int:
    # return the number of active of bookings for room
    number_of_active_bookings_in_room = Booking.objects.filter(room=room_instance, end_time__gt=timezone.now()).count()
    return number_of_active_bookings_in_room

def active_tenants(room_instance: RoomProfile) -> int:
    # return the number of active tenants in room
    campus_end_year = room_instance.campus.end_of_acadamic_year
    number_of_active_tenants_in_room = Tenant.objects.filter(room=room_instance, end_date__gt=campus_end_year).count()
    return number_of_active_tenants_in_room

def capacity_available(room_instance: RoomProfile) -> bool:
    # count all tenants in room
    campus_end_year = room_instance.campus.end_of_acadamic_year
    count_members = Tenant.objects.filter(room=room_instance, end_date__gt=campus_end_year).count()
    if room_instance.bed_space_left <= count_members:
        """
        Room will likely not show for booking but incase it shows
        """
        room_instance.occupied =True
        room_instance.save()
        # return false is not available
        return False
    elif room_instance.bed_space_left <= 0:
        """
        Could be possible that room bed space is less than
        or equal to 0 which means room is not
        available
        """
        room_instance.occupied =True
        room_instance.save()
        # return false is not available
        return False
    else:
        # if room is not full with tenants
        return True