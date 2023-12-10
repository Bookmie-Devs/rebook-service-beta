from collections.abc import Iterable
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
from django.utils.translation import gettext_lazy as _
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
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)
    payed = models.BooleanField(default=False) 
    class Meta:
        ordering = ('-start_time',)

    def delete_if_not__valid(self):
        query = Booking.objects.get(booking_id=self.booking_id)
        query.delete()
    
    def save(self, *args, **kwargs):
        """
        using timezone.now() instead of start_time because
        start usese auto_now_add which is NoneType until the
        the data is saved to the database
        """
        self.end_time = (timezone.now() + timedelta(minutes=60))
        return super().save(*args, **kwargs)

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
                                        unique=True,
                                        editable=False)
    
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    class Meta:
        ordering = ('-start_date',)

    def save(self, *args, **kwargs):
        """
        using timezone.now() instead of start_time because
        start usese auto_now_add which is NoneType until the
        the data is saved to the database
        """
        if self.start_date is None:
            # use time zone if start-time is not set yet
            self.end_date = (timezone.now() + timedelta(days=365))
        else:
            self.end_date = (self.start_date + timedelta(days=365))

        ############### ( ⚠️Critcal) verification code
        self.verification_code = f'{self.hostel.hostel_code}-0{self.end_date.day}r0-{self.user.first_name[:2]}-0{self.end_date.month}b0-{self.user.last_name[:3]}-{self.tenant_id}-{self.user.first_name.lower()}-{self.user.student_id}-07{self.end_date.year}k0-{self.user.last_name.lower()}-{self.end_date.time()}-Grj'.replace(" ","")
        return super().save(*args, **kwargs)
    
    def is_active(self):
        # check if user time is up and needs to update V-code
        return timezone.now().date() < self.end_date.date()
    
    def delete_if_expired(self):
        if not self.is_active():
            self.delete()
    
    def __str__(self):
        return f'{self.user}'

class NewsletterEmails(models.Model):
    email = models.EmailField()
    class Meta:
        verbose_name = _("News letter Emails")
        verbose_name_plural = _("News letters Emails")

    def __str__(self):
        return self.email

class NewsLetterMessage(models.Model):
    subject = models.TextField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date

class GeneralNewsLetter(models.Model):
    subject = models.TextField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date