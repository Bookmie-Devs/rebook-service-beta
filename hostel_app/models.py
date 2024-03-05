from django.db import models
from campus_app.models import CampusProfile
import uuid
from random import randint
from django.utils import timezone
from config import sms
from django.utils.translation import gettext_lazy as _
from accounts.task import send_sms_task
from django.urls import reverse
from accounts.models import CustomUser
from agents_app.models import Agent
from django_google_maps import fields as map_fields


Banks = [
    ("280100", "Access Bank"),
    ("080100", "ADB Bank Limited"),
    ("030100","Absa Bank Ghana Ltd"),
    ("MTN", "MTN"),
    ("VOD", "Vodafone"),
    ("ATL", "AirtelTigo"),
    ("070101","ARB Apex Bank"),
    ("210100", "Bank of Africa Ghana"),
    ("010100", "Bank of Ghana"),
    ("300335", "Best Point Savings and Loans"),
    ("140100", "CAL Bank Limited"),
    ("340100", "Consolidated Bank Ghana Limited"),
    ("130100", "Ecobank Ghana Limited"),
    ("200100", "FBNBank Ghana Limited"),
    ("240100", "Fidelity Bank Ghana Limited"),
    ("170100", "First Atlantic Bank Limited"),
    ("330100", "First National Bank Ghana Limited"),
    ("040100", "GCB Bank Limited"),
    ("230100", "Guaranty Trust Bank (Ghana) Limited"),
    ("050100", "National Investment Bank Limited"),
    ("360100", "OmniBSCI Bank"),
    ("180100","Prudential Bank Limited"),
    ("110100", "Republic Bank (GH) Limited"),
    ("300361", "Services Integrity Savings and Loans"),
    ("090100", "Société Générale Ghana Limited"),
    ("190100", "Stanbic Bank Ghana Limited"),
    ("020100", "Standard Chartered Bank Ghana Limited"),
    ("060100", "United Bank for Africa Ghana Limited"),
    ("100100", "Universal Merchant Bank Ghana Limited"),
    ("120100", "Zenith Bank Ghana"),]

category =[('Hostel','Hostel'),('Homestel','Homestel'),
                             ('Apartment','Apartment')]

# Function to generate hostel code
def genrate_hostel_code()-> str:
    code = f"BH{randint(10000, 99999)}"
    while HostelProfile.objects.filter(hostel_code=code).exists():
         code = f"BH{randint(10000, 99999)}"
    return code

'''Hostel model for database'''
class HostelProfile(models.Model): 
    hostel_name = models.CharField(max_length=50)
    # NOT THE PRIMARY KEY
    hostel_code = models.CharField(max_length=7, default=genrate_hostel_code, unique=True)
    hostel_image = models.ImageField(upload_to='HostelProfiles',
                                      default='unavailable.jpg')
    hostel_image2 = models.ImageField(upload_to='HostelProfiles',
                                      default='unavailable.jpg')
    hostel_image3 = models.ImageField(upload_to='HostelProfiles',
                                      default='unavailable.jpg')
    hostel_image4 = models.ImageField(upload_to='HostelProfiles',
                                      default='unavailable.jpg')
    hostel_image5 = models.ImageField(upload_to='HostelProfiles',
                                      default='unavailable.jpg')
    # room image of the hostel
    room_image =  models.ImageField(upload_to='RoomImages',verbose_name="Image of one room",
                                      default='unavailable.jpg')
    room_image2 = models.ImageField(upload_to='RoomImages',verbose_name="Image2 of one room",
                                      default='unavailable.jpg')
    room_image3 = models.ImageField(upload_to='RoomImages',verbose_name="Image3 of one room",
                                      default='unavailable.jpg')
    room_image4 = models.ImageField(upload_to='RoomImages',verbose_name="Image4 of one room",
                                      default='unavailable.jpg')
    room_image5 = models.ImageField(upload_to='RoomImages',verbose_name="Image5 of one room",
                                      default='unavailable.jpg')
    room_image6 = models.ImageField(upload_to='RoomImages',verbose_name="Image6 of one room",
                                      default='unavailable.jpg')
    
    category = models.CharField(max_length=15, verbose_name='type',default='Hostel', blank=False, choices=category)
    
    no_of_likes = models.IntegerField(verbose_name='Likes', default=7)
    
    price_range = models.CharField(max_length=50, default='unavailable', blank=True)
    
    number_of_rooms = models.IntegerField(default=5)
    campus = models.ForeignKey(CampusProfile, on_delete=models.SET_NULL, null=True)

    hostel_manager = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, related_name='hostels', null=True, blank=True)
    hostel_manager_profile_picture = models.ImageField(upload_to='Management Images',verbose_name="Manager Profile", default='unavailable.jpg')
    agent_affiliate = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    hostel_email = models.EmailField(blank=True, null=True)

    account_number = models.CharField(max_length=70, default='unavailable',)

    #Bank code for momo is MTN IF not specified
    bank_code = models.CharField(max_length=50, choices=Banks ,default='unavailable')

    mobile_money = models.CharField(max_length=14, default='unavailable',)
    
    manager_contact = models.CharField(max_length=10, blank=True, verbose_name="Manager's Contact")

    hostel_contact = models.CharField(max_length=10, verbose_name="Hostel's Contact")

    other_contact = models.CharField(max_length=10, blank=True)

    location = models.CharField(max_length=500, default="location unavailable")

    main_website = models.URLField(_("Main Website"), max_length=200, null=True, blank=True)
    verified = models.BooleanField(default=False)
    occupied = models.BooleanField(default=False)
   
    #Location of hostel base on Google map API
    address = map_fields.AddressField(max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=500, blank=True, null=True)

    facilities = models.TextField(default="unavailable")

    send_management_sms = models.BooleanField(default=False)
    message = models.TextField(default="Type New Message")

    class Meta:
        db_table = 'hostel_profiles'
        
        ordering = ('-hostel_name',)
    

    def save(self, *args, **kwargs):
        if self.send_management_sms and self.verified:
            msg = self.message
            # send_sms_task.delay(self.manager_contact,msg)
            sms.send_sms_message(self.manager_contact,msg)
            self.send_management_sms = False
            self.message = "Type New Message"

        return super().save(*args, **kwargs)


    def get_profile_url(self):
        return reverse("hostels:profile", kwargs={'hostel_code':self.hostel_code})


    def get_rooms(self):
        return reverse("hostels:hostel-rooms", kwargs={"hostel_code":self.hostel_code})
    

    def __str__(self):
        return f'{self.hostel_name}'
    

class HostelManagement(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    management_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    management_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    profile_picture =models.ImageField(upload_to='Management Images',verbose_name="Management Profile",default='unavailable.jpg')
    hostel = models.OneToOneField(HostelProfile, on_delete=models.SET_NULL, related_name='hostels', null=True,)
    is_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.management_code = f"{self.user.first_name[:3]}{self.user.last_name[:3]}{str(self.management_id)[:6]}"
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username}@{self.hostel.hostel_name}"
    


class SalesStatistics(models.Model):
    hostel = models.ForeignKey(HostelProfile, on_delete=models.PROTECT)
    date = models.DateField(_("date recorded"), auto_now=False, auto_now_add=True)
    last_updated = models.DateField(_("last updated"), auto_now=True, auto_now_add=False)
    year = models.PositiveIntegerField(default=timezone.now().year)
    amount_made = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = _("Sales Stat")
        verbose_name_plural = _("Sale Stats")

    def __str__(self):
        return f"{self.hostel.hostel_name} on {self.year}"
