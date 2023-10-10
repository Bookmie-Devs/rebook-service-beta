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
    floor_no = models.CharField(max_length=20, default=0,
                                verbose_name='Floor number')

    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.CASCADE, 
                               related_name='rooms')
    
    campus = models.ForeignKey(CampusProfile, on_delete=models.SET_NULL,
                                verbose_name="Campus where Room is located",
                                null=True)
    
    room_capacity = models.PositiveIntegerField(default=4)
    room_img = models.ImageField(upload_to='RoomImages', default='unavailable.jpg')
    room_price = models.DecimalField(blank=False, decimal_places=1, max_digits=7 )
    
    rating = models.IntegerField(choices=rating ,blank=False, 
                                 default='⭐', )
    
    # occupied by users who booked but not payed yet
    booking_occupied = models.BooleanField(default=False)

    # actually occupied by tenants
    occupied = models.BooleanField(default=False)

    #room features
    contains_kitchen = models.BooleanField(default=False)
    shared_kitchen = models.BooleanField(default=False)

    """ if room does not contain bathroom then it is shared """
    contains_bathroom = models.BooleanField(default=False)

    air_condition = models.BooleanField(default=False)



    class Meta:
        db_table = "room_profiles"

    def get_profile_url(self):
        return reverse("rooms:profile", kwargs={'room_id':self.room_id})

    def __str__(self):
        return f'Room {self.room_no} in {self.hostel} @{self.campus}' 


