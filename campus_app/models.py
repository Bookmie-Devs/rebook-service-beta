from collections.abc import Iterable
from typing import Any, Type
from django_google_maps import fields as map_fields
from django.db import models
from django.utils import timezone
import uuid

# no module 'django.utils.six' to make this package work
# from geoposition.fields import GeopositionField
# Create your models here.

class CampusProfile(models.Model):
    campus_name = models.CharField(max_length=100)
    # name known to the public
    alias_name =  models.CharField(max_length=100, blank=True, null=True)
    campus_code = models.CharField(max_length=100, unique=True)
    flag = models.ImageField(default='defaultFlag.jpg', upload_to='CampusFlag')
    available_on_campus = models.BooleanField(default=False, verbose_name="Bookmie.com Working on Campus")
    location = models.CharField(max_length=255, null=True, blank=True)
    address = map_fields.AddressField(max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=500, blank=True, null=True)
    end_of_acadamic_year = models.DateField(null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.campus_name}'

    def save(self, *args, **kwargs) -> None:
        self.campus_code = self.campus_code.upper().strip()
        return super().save(*args, **kwargs)
    

class CollegeProfile(models.Model):
    college_name = models.CharField(max_length=100)
    college_id = models.CharField(max_length=100, unique=True)
    campus_name = models.ForeignKey(CampusProfile, on_delete=models.CASCADE,)
    address = map_fields.AddressField(max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=500, blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.college_name}'
    
