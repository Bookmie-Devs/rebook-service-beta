from django.conf import settings
from django.db import models
from hostel_app.models import HostelProfile
from campus_app.models import CampusProfile
from django.utils import timezone
from accounts.models import CustomUser
import uuid
from django.urls import reverse
from datetime import datetime

class RoomProfile(models.Model):
    # room number
    room_no = models.CharField(max_length=20,default=000,verbose_name='Room number')
    # floor number of room
    floor_no = models.IntegerField(default=0,verbose_name='Floor number')

    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.CASCADE, 
                               related_name='rooms')
    
    campus = models.ForeignKey(CampusProfile, on_delete=models.SET_NULL,
                                verbose_name="Campus where Room is located",
                                null=True)
    
    room_capacity = models.PositiveIntegerField(default=4)
    bed_space_left = models.IntegerField(default=0)

    gender = models.CharField(max_length=20,
                            choices=[('female','female'),('male','male'),('open','open')],
                            verbose_name="Gender of room",
                            default="open")
    # managers price
    room_price = models.DecimalField(blank=False, decimal_places=2, max_digits=8)
    # platform pricing(selling price)
    ptf_room_price = models.DecimalField(default=0.0, editable=False, decimal_places=2, max_digits=8)
    # for half payment
    half_pricing = models.DecimalField(default=0.0, editable=False, decimal_places=2, max_digits=8)
    """
    field just there to compare and check if the field "room price"
    has been changed or not when the save method is called on an object
    """
    accept_half_payment =  models.BooleanField(default=False)
    previous_price_check = models.DecimalField(blank=True, editable=False, null=True, decimal_places=2, max_digits=7)
    no_of_likes = models.IntegerField(verbose_name='Likes', default=1)
    # count the number of users who book this room
    booking_count = models.PositiveIntegerField(default=0)
    # occupied by users who booked but not payed yet
    booking_occupied = models.BooleanField(default=False)
    #check if room is occupied through platform
    platform_occupied = models.BooleanField(default=False)
    # actually occupied by tenants(managers check) 
    occupied = models.BooleanField(default=False)
    #room features
    inbuilt_kitchen = models.BooleanField(default=False)
    """ if room does not contain bathroom then it is shared """
    inbuilt_bathroom = models.BooleanField(default=False)

    inbuilt_balcony = models.BooleanField(default=False)
    air_condition = models.BooleanField(default=False)
    is_free =  models.BooleanField(default=False)

    verified = models.BooleanField(default=False)
    class Meta:
        db_table = "room_profiles"

    def save(self, *args, **kwargs):
        # CHECK IF ROOM PRICE IS SAME A PREVIOUS PRICE IF NOT UPDATE FIELDS
        # Without this check, anytime the save method is called the pft_room_price will
        # and upadte itself.
        if self.room_price!=self.previous_price_check:
            addtional_pricing: float = float(self.room_price) * settings.SUPPLY_COST_PERCENTAGE
            # additional price for half payment
            addtional_half_pricing: float = float(self.room_price/2) * settings.SUPPLY_COST_PERCENTAGE
            # new prices
            self.ptf_room_price = float(self.room_price) + addtional_pricing
            self.half_pricing = float(self.room_price/2) + addtional_half_pricing
            # equate the two to maintain the balance
            self.previous_price_check = self.room_price
        else:
            """
            Do nothing to ptf price if room price is still the same,
            could be that the room has been updated but not the 
            price which does not need to be updated
            """
            pass
        return super().save(*args, **kwargs)
    
    def reduce_bed_spaces(self, count_members:int=None):
        """
        decrease room bed space after tenant has payed
        before checking if bed sapce is less than zero
        """
        self.bed_space_left = self.bed_space_left - 1
        self.save()
        # check if room is full by comparing the number of active tenants
        """
        count memebers counts the number of tenants in the room
        and trigger occupied if greater than room capacity
        """
        if self.room_capacity <= count_members or self.bed_space_left <= 0:
            self.bed_space_left = 0
            self.occupied = True
            self.save()
    
            
    def is_available_for_booking(self) -> bool:
        # check and compare if booking is available for the room

        from .room_checks import active_bookings, active_tenants
        """
        import fuctions here to avoid circular import errors with
        Tenants and Booking class
        """
        available: bool = active_bookings(self) < self.bed_space_left
        """
        Check if the active bookings is less than the bed sapces left
        if it is then meaning there is space avaialable for booking
        """
        return available

    def is_space_available(self):
        # check in advance if room is not full
        from .room_checks import capacity_available
        """
        import fuctions here to avoid circular import errors with
        Tenants and Booking class
        """
        available: bool = capacity_available(self)
        return available

    def change_room_gender(self, members, user_gender:str):
        if members==1 and self.gender.lower()=='open':
            self.gender=user_gender.lower()
            self.save()
        else:
            pass

    def get_detail_url(self):
        return reverse("rooms:profile", kwargs={'room_id':self.room_id})

    def __str__(self):
        return f'Room {self.room_no} in {self.hostel} @{self.campus}' 


