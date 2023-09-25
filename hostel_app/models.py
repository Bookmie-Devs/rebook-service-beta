from django.db import models
from campus_app.models import CampusProfile
# from geoposition.fields import GeopositionField
import uuid
from accounts.models import CustomUser

rating = [('⭐⭐⭐⭐','4-stars'),
           ('⭐⭐⭐','3-stars'),
           ('⭐⭐','2-stars'),
           ('⭐','1-star')]

Hostel_Type =[
              ('Hostel🏢','Hostel'),
              ('Homestel🏠','Homestel'),
              ('Apartment💰','Apartment')]

class HostelProfile(models.Model): 
    '''Hostel model for database'''
    hostel_name = models.CharField(max_length=50)
    hostel_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hostel_code = models.CharField(max_length=50, null=True)
    hostel_image = models.ImageField(upload_to='Hostel_Profiles', default='unavailable.jpg')

    type_of_hostel = models.CharField(max_length=15,
                                     verbose_name='Type',default='Hostel',
                                     blank=False, choices=Hostel_Type)
    
    rating = models.CharField(max_length=20, choices=rating,
                                       verbose_name='Stars',
                                       default='1-star')
    
    hostel_rating = models.IntegerField(default=0)
    price_range = models.CharField(max_length=50, default='unavailable', blank=True)
    hostel_motto = models.CharField(max_length=2000, blank=True)
    number_of_rooms = models.IntegerField(default=5)
    campus = models.ForeignKey(CampusProfile, on_delete=models.SET_NULL, null=True)
    hostel_manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
                                       related_name='hostels', null=True,)
    hostel_email = models.EmailField(blank=True)
    bank_details = models.CharField(max_length=20)
    mobile_money = models.CharField(max_length=14)
    managers_contact = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=10)
    hostel_location_specification = models.CharField(max_length=500, blank=True)
    other_phone = models.CharField(max_length=10, blank=True)
    on_map_location = models.CharField(max_length=10000,default='unavailable')
    hostel_main_site = models.URLField(null=True, blank=True)
    #Location of hostel base on Google map API
    address = models.CharField(max_length=255)
    # Hostel_Location = GeopositionField(blank = True)
    verified = models.BooleanField(default=False)
    occupied = models.BooleanField(default=False)

    class Meta:
        db_table = 'hostel_profiles'

    def __str__(self):
        return f'{self.hostel_name} Profile'
    

