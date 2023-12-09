from django.conf import settings
from django.db import models
from hostel_app.models import HostelProfile
from campus_app.models import CampusProfile
from accounts.models import CustomUser
from hostel_app.models import rating
import uuid
from django.urls import reverse
from datetime import datetime

class RoomProfile(models.Model):
    # room number
    room_no = models.CharField(max_length=20,default=000,
                               verbose_name='Room number')
    # floor number of room
    floor_no = models.IntegerField(default=0,
                                verbose_name='Floor number')

    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.CASCADE, 
                               related_name='rooms')
    
    campus = models.ForeignKey(CampusProfile, on_delete=models.SET_NULL,
                                verbose_name="Campus where Room is located",
                                null=True)
    
    room_capacity = models.PositiveIntegerField(default=4)
    bed_space_left = models.PositiveIntegerField(default=0)

    gender = models.CharField(max_length=20,
                            choices=[('female','female'),('male','male')],
                            verbose_name="Gender of room",
                            default="male")
    # managers price
    room_price = models.DecimalField(blank=False, decimal_places=1, max_digits=8)
    # platform pricing(selling price)
    ptf_room_price = models.DecimalField(default=0.0, editable=False, decimal_places=1, max_digits=8)
    # field just there to compare and check if field room price has been changed on save
    previous_price_check = models.DecimalField(blank=True, editable=False,
                                      null=True, decimal_places=1, max_digits=7)

    rating = models.IntegerField(choices=rating ,blank=False, 
                                 default='⭐', )
    
    # occupied by users who booked but not payed yet
    booking_occupied = models.BooleanField(default=False)

    # actually occupied by tenants
    occupied = models.BooleanField(default=False)

    #room features
    inbuilt_kitchen = models.BooleanField(default=False)

    """ if room does not contain bathroom then it is shared """
    inbuilt_bathroom = models.BooleanField(default=False)

    inbuilt_balcony = models.BooleanField(default=False)
    air_condition = models.BooleanField(default=False)

    class Meta:
        db_table = "room_profiles"

    def save(self, *args, **kwargs):
        # CHECK IF ROOM PRICE IS SAME A PREVIOUS PRICE IF NOT UPDATE FIELDS
        if self.room_price!=self.previous_price_check:
            addtional_pricing: float = float(self.room_price) * settings.SUPPLY_COST_PERCENTAGE
            self.ptf_room_price = float(self.room_price) + addtional_pricing
            # equate the two to maintain the balance
            self.previous_price_check = self.room_price
        else:
            pass
        return super().save(*args, **kwargs)
    
    def check_bed_spaces(self, count_members:int=None):
        # check if room is full by comparing the number of active tenants
        if self.room_capacity <= count_members or self.bed_space_left <= 0:
            self.bed_space_left = 0
            self.occupied = True
            self.save()
        else:
            # decrease bed space 
            self.bed_space_left -= 1
            self.save()

    def get_detail_url(self):
        return reverse("rooms:profile", kwargs={'room_id':self.room_id})

    def __str__(self):
        return f'Room {self.room_no} in {self.hostel} @{self.campus}' 


