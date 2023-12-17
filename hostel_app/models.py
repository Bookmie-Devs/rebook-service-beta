from django.db import models
from campus_app.models import CampusProfile
import uuid
from django.urls import reverse
from accounts.models import CustomUser
from django_google_maps import fields as map_fields


rating = [(4,'⭐⭐⭐⭐'),(3,'⭐⭐⭐'),
                 (2,'⭐⭐'), (1,'⭐')]

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

class HostelProfile(models.Model): 

    '''Hostel model for database'''
    hostel_name = models.CharField(max_length=50)

    hostel_id = models.UUIDField(default=uuid.uuid4, 
                                 editable=False, unique=True)
    
    hostel_code = models.CharField(max_length=100,
                                   null=True, blank=True,
                                   unique=True)

    hostel_image = models.ImageField(upload_to='HostelProfiles',
                                      default='unavailable.jpg')
    # for hostel managers
    hostel_manager_profile_picture = models.ImageField(default="unknown_profile.jpg", upload_to="ManagersProfilePictures")

    # room image of the hostel
    room_image =  models.ImageField(upload_to='RoomImages',verbose_name="Image of one room",
                                      default='unavailable.jpg')

    category = models.CharField(max_length=15,
                                    verbose_name='type',default='Hostel',
                                    blank=False, choices=category)

    rating = models.IntegerField(choices=rating, verbose_name='Stars',
                                       default=1)
    
    price_range = models.CharField(max_length=50, 
                                   default='unavailable', 
                                   blank=True)
    
    number_of_rooms = models.IntegerField(default=5)
    campus = models.ForeignKey(CampusProfile, on_delete=models.SET_NULL, null=True)

    hostel_manager = models.OneToOneField(CustomUser, on_delete=models.SET_NULL,
                                          related_name='hostels', null=True,)
    
    hostel_email = models.EmailField(blank=True)

    account_number = models.CharField(max_length=70,
                                      default='unavailable',)

    #Bank code for momo is MTN IF not specified
    bank_code = models.CharField(max_length=50, choices=Banks ,default='unavailable')

    mobile_money = models.CharField(max_length=14,
                                    default='unavailable',)
    
    manager_contact = models.CharField(max_length=10, blank=True,
                                       verbose_name="Manager's Contact")

    hostel_contact = models.CharField(max_length=10, verbose_name="Hostel's Contact")

    other_contact = models.CharField(max_length=10, blank=True)

    location = models.CharField(max_length=500, default="location unavailable")

    
    main_website = models.URLField(null=True, blank=True, 
                                verbose_name='Hostel Website')

    verified = models.BooleanField(default=False)
    occupied = models.BooleanField(default=False)
   
    #Location of hostel base on Google map API
    address = map_fields.AddressField(max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=500, blank=True, null=True)

    facilities = models.TextField(default="unavailable")

    class Meta:
        db_table = 'hostel_profiles'
        
        ordering = ('-hostel_name',)
    

    def save(self, *args, **kwargs):

        #  create hostel code on save
        self.hostel_code = f'{self.hostel_name[:3].upper()}{str(self.hostel_id)[:4]}'

        return super().save(*args, **kwargs)


    def get_profile_url(self):
        return reverse("hostels:profile", kwargs={'hostel_id':self.hostel_id})


    def get_rooms(self):
        return reverse("hostels:hostel-rooms", kwargs={"hostel_id":self.hostel_id})
    

    def __str__(self):
        return f'{self.hostel_name}'
    
