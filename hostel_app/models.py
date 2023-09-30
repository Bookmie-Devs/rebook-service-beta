from django.db import models
from campus_app.models import CampusProfile
# from geoposition.fields import GeopositionField
import uuid
from django.urls import reverse
from accounts.models import CustomUser

rating = [('⭐⭐⭐⭐','⭐⭐⭐⭐'),('⭐⭐⭐','⭐⭐⭐'),
           ('⭐⭐','⭐⭐'), ('⭐','⭐')]

category =[('Hostel','Hostel'),('Homestel','Homestel'),
            ('Apartment','Apartment')]

class HostelProfile(models.Model): 
    '''Hostel model for database'''
    hostel_name = models.CharField(max_length=50)

    hostel_id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                                 editable=False, unique=True)
    
    hostel_code = models.CharField(max_length=50, null=True)

    hostel_image = models.ImageField(upload_to='Hostel_Profiles',
                                      default='unavailable.jpg')

    category = models.CharField(max_length=15,
                                    verbose_name='type',default='Hostel',
                                    blank=False, choices=category)

    rating = models.CharField(max_length=10,choices=rating, verbose_name='Stars',
                                       default='⭐')
    
    price_range = models.CharField(max_length=50, 
                                   default='unavailable', 
                                   blank=True)
    
    hostel_motto = models.CharField(max_length=2000, blank=True)
    number_of_rooms = models.IntegerField(default=5)
    campus = models.ForeignKey(CampusProfile, on_delete=models.SET_NULL, null=True)

    hostel_manager = models.OneToOneField(CustomUser, on_delete=models.SET_NULL,
                                          related_name='hostels', null=True,)
    
    hostel_email = models.EmailField(blank=True)
    account_number = models.CharField(max_length=50, default='unavailable')

    #Bank code for momo is MTN IF not specified
    bank_code = models.CharField(max_length=50, default='unavailable')

    mobile_money = models.CharField(max_length=14, default='unavailable')
    managers_contact = models.CharField(max_length=10, blank=True)
    contact = models.CharField(max_length=10)
    location = models.CharField(max_length=500, default="location unavailable")
    other_phone = models.CharField(max_length=10, blank=True)
    map_location = models.CharField(max_length=10000, default='unavailable')
    hostel_main_site = models.URLField(null=True, blank=True)
    
    #Location of hostel base on Google map API
    address = models.CharField(max_length=255)
    # Hostel_Location = GeopositionField(blank = True)
    verified = models.BooleanField(default=False)
    occupied = models.BooleanField(default=False)

    class Meta:
        db_table = 'hostel_profiles'
        
        ordering = ('-hostel_name',)

    def get_profile_url(self):
        return reverse("hostels:profile", kwargs={'hostel_id':self.hostel_id})


    def get_rooms(self):
        return reverse("hostels:hostel-rooms", kwargs={"hostel_id":self.hostel_id})
    

    def __str__(self):
        return f'{self.hostel_name}'
    

