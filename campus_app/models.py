from collections.abc import Iterable
from random import randint
from typing import Any, Type
from django_google_maps import fields as map_fields
from django.db import models
from django.utils import timezone
import uuid

# no module 'django.utils.six' to make this package work
# from geoposition.fields import GeopositionField
# Create your models here.

class CampusProfile(models.Model):
    campus_name = models.CharField(max_length=50)
    campus_param_id = models.CharField(max_length=50, editable=False, null=True)
    # name known to the public
    alias_name =  models.CharField(max_length=10, blank=True, null=True)
    campus_code = models.CharField(max_length=6, unique=True)
    flag = models.ImageField(default='defaultFlag.jpg', upload_to='CampusFlag')
    available_on_campus = models.BooleanField(default=False, verbose_name="Bookmie.com Working on Campus")
    location = models.CharField(max_length=255, null=True, blank=True)
    address = map_fields.AddressField(max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True, null=True)
    end_of_acadamic_year = models.DateTimeField(null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.campus_name}'

    def save(self, *args, **kwargs) -> None:
        code = f'verified-{self.campus_code.title()}#bookmie.com#Registered'
        self.campus_param_id = code.strip()
        return super().save(*args, **kwargs)
    

class CollegeProfile(models.Model):
    college_name = models.CharField(max_length=20)
    college_code = models.CharField(max_length=10, null=True)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE,)
    address = map_fields.AddressField(max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.college_name}'
    
