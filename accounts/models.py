from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from campus_app.models import CampusProfile
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .task import send_sms_task
from django.template.loader import render_to_string
import uuid


#User extention
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=50, null=True, blank=True,)
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(blank=False, unique=True)
    phone = models.CharField(max_length=10, blank=False)
    gender = models.CharField(max_length=7, default='')

    is_student = models.BooleanField(default=False)
    # is a hostel manager ot not
    is_hostel_manager = models.BooleanField(default=False, verbose_name="Manager")
    
    # is a hostel worker not manager(work at the hostel/Porter)
    is_hostel_worker = models.BooleanField(default=False, verbose_name='Hostel Woker')
    
    # is a hostel worker not manager(work at the hostel agent)
    is_hostel_agent = models.BooleanField(default=False, verbose_name='Hostel Agent')

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
        self.phone = str(self.phone).strip()
        self.email = str(self.email).strip()

        if self.middle_name != "":
            self.username=f"{self.first_name.capitalize()} {self.middle_name.capitalize()} {self.last_name.capitalize()}"
            
        else:
            self.username=f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

        return super().save(*args,**kwargs)
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name=_("User"), on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, blank=False, unique=True)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE, null=True)
    college = models.CharField(max_length=70, blank=True, null=True)
    
    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students") 

    def save(self, *args, **kwargs) -> None:
        self.student_id = str(self.student_id).strip()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("Student_detail", kwargs={"pk": self.pk})

class OtpCodeData(models.Model):
    otp_code_id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    otp_code = models.CharField(_("OTP CODE"), max_length=50, blank=True, null=True)
    user =  models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    code_life_time = models.DateTimeField(_("code life time"),auto_now=False,auto_now_add=False,blank=True,null=True)

    def save(self, *args, **kwargs) -> None:
        from random import randint
        code = randint(100000,999999)
        while OtpCodeData.objects.filter(otp_code=code).exists():
            code = randint(100000,999999)
        self.otp_code=code
        self.code_life_time = timezone.now() + timezone.timedelta(minutes=10)
        return super().save(*args, **kwargs)
    
    def has_expired(self):
        return self.code_life_time <= timezone.now()
    
    class Meta:
        verbose_name = _("OtpCodeData")
        verbose_name_plural = _("OtpCodeDatas")

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("OtpData_detail", kwargs={"pk": self.pk})
