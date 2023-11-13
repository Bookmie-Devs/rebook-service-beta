from collections.abc import Iterable
from typing import Any, Type
from django.db import models
import uuid
# from geoposition.fields import GeopositionField
# Create your models here.

class CampusProfile(models.Model):
    campus_name = models.CharField(max_length=100)
    campus_code = models.CharField(max_length=100, unique=True)
    flag = models.ImageField(default='defaultFlag.jpg', upload_to='CampusFlag')
    address = models.CharField(max_length=255)
    # location= GeopositionField(max_length=42)

    def __str__(self) -> str:
        return f'{self.campus_name}'

    def save(self, *args, **kwargs) -> None:
        self.campus_code = self.campus_code.upper().strip()
        return super().save(*args, **kwargs)
    

class CollegesProfile(models.Model):
    college_name = models.CharField(max_length=100)
    college_id = models.CharField(max_length=50)
    campus_name = models.ForeignKey(CampusProfile, on_delete=models.CASCADE,)
    address = models.CharField(max_length=90)
    # location = GeopositionField(max_length=42)
    
    def __str__(self) -> str:
        return f'{self.college_name}'
    
