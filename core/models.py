from django.db import models
from django.contrib.auth.models import AbstractUser
from rooms_app.models import RoomProfile
from django.utils import timezone 
from django.utils.timezone import timedelta
from datetime import datetime
from hostel_app.models import HostelProfile
from campus_app.models import CampusProfile
import asyncio
from datetime import datetime
import asyncio
from accounts.models import CustomUser
import uuid
#Booking model
# no
class Booking(models.Model):
    room = models.ForeignKey(RoomProfile, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.CASCADE)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20)
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    payed = models.BooleanField(default=False) 
    class Meta:
        ordering = ('-start_time',)

    def delete_if_not__valid(self):
        query = Booking.objects.get(booking_id=self.booking_id)
        query.delete()
       
    def __str__(self):
        return f'{self.user} || {self.room}'

#Payed for booking
class Tenant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tenant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    room = models.ForeignKey(RoomProfile, on_delete=models.CASCADE)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.CASCADE)
    payed = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)

    # verification_code for tenant
    verification_code = models.CharField(max_length=700,
                                        default='unavailable', 
                                        unique=True,)
    
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    class Meta:
        ordering = ('-start_date',)

    def save(self, *args, **kwargs):
        self.end_date = (timezone.now()+timedelta(days=365))

        # verification code
        self.verification_code = f'{self.hostel.hostel_code}-{self.user.first_name[:2]}-009-{self.user.last_name[:3]}-{self.tenant_id}-{self.user.first_name.upper()}-{self.user.student_id}-{self.user.last_name.upper()}'

        return super().save(*args, **kwargs)
    
    def is_active(self):
        return datetime.now() <= self.end_date
    
    def delete_if_expired(self):
        if not self.is_active():
            self.delete()
    
    def __str__(self):
        return f'{self.user}'
