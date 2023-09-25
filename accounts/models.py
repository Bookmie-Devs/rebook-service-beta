from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from campus_app.models import CampusProfile
import uuid


#User extention
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=50, null=True,
                                   blank=True)
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(blank=False, unique=True)
    phone = models.CharField(max_length=10, blank=False)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE, null=True)
    college = models.CharField(max_length=70, blank=False)
    gender = models.CharField(max_length=7, null=True, blank=True)
    student_id = models.CharField(max_length=20, blank=False)

    def __str__(self) -> str:
        return f'{self.username}'
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name','last_name','username'] 

    """overwrite the save method to change and merge the first name and last_name
    into username"""
    
    def save(self, *args, **kwargs) -> None:
        if self.middle_name is not None:
            self.username=f"{self.first_name.upper()}_{self.middle_name} {self.last_name}"
        else:
            self.username=f"{self.first_name.upper()}_{self.last_name}"
        return super().save(*args,**kwargs)
    



