from django.db import models
from hostel_app.models import HostelProfile
from campus_app.models import CampusProfile
from accounts.models import CustomUser
from hostel_app.models import rating
import uuid
from datetime import datetime

class RoomProfile(models.Model):
    room_no = models.CharField(max_length=20,default=000)
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.CASCADE, 
                               related_name='rooms')
    
    campus = models.ForeignKey(CampusProfile, on_delete=models.SET_NULL,
                                verbose_name="Campus where Room is located",
                                null=True)
    
    room_capacity = models.PositiveIntegerField(default=4)
    room_img = models.ImageField(upload_to='RoomImages', default='unavailable.jpg')
    room_price = models.DecimalField(blank=False, decimal_places=1, max_digits=7 )
    
    rating = models.CharField(choices=rating ,blank=False, default='⭐',
                                                            max_length=15)
    occupied = models.BooleanField(default=False)


    class Meta:
        db_table = "room_profiles"

    def __str__(self):
        return f'Room {self.room_no} in {self.hostel} @{self.campus}' 


