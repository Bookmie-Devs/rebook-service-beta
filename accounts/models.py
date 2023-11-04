from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from campus_app.models import CampusProfile
import uuid


#User extention
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=50, null=True,
                                   blank=True,)
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(blank=False, unique=True)
    phone = models.CharField(max_length=10, blank=False)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE, null=True)
    college = models.CharField(max_length=70, blank=False)
    gender = models.CharField(max_length=7, null=True, blank=True)
    student_id = models.CharField(max_length=20, blank=False)
    
    # is a hostel manager ot not
    is_hostel_manager = models.BooleanField(default=False, verbose_name="manager")

    # is a hostel worker not manager(work at the hostel/Porter)
    is_hostel_worker = models.BooleanField(default=False, verbose_name='Hostel Woker')

    def __str__(self) -> str:
        return f'{self.username}'
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name','last_name','username'] 

    """overwrite the save method to change and merge the first name and last_name
    into username"""

    def save(self, *args, **kwargs) -> None:

        # strip off all blank spaces in fields
        self.first_name = str(self.first_name).strip()
        self.middle_name = str(self.middle_name).strip()
        self.last_name = str(self.last_name).strip()
        self.student_id = str(self.student_id).strip()
        self.phone = str(self.phone).strip()
        self.email = str(self.email).strip()

        if self.middle_name == "":
            self.username=f"{self.first_name.capitalize()} {self.middle_name.capitalize()} {self.last_name.capitalize()}"
            
        else:
            self.username=f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

        return super().save(*args,**kwargs)
    



