from django.db import models
from django.urls import reverse
import uuid
from campus_app.models import CampusProfile
from django.utils.translation import gettext_lazy as _
from django_google_maps import fields as map_fields
from accounts.models import CustomUser
# Create your models here.


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



class GuestHouse(models.Model):
    guest_house_name = models.CharField(max_length=100)
    house_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    house_code = models.CharField(max_length=100,null=True, blank=True,unique=True)
    house_image = models.ImageField(upload_to='GuestHouseImage',default='unavailable.jpg')
    campus = models.ForeignKey(CampusProfile, on_delete=models.PROTECT)
    phone = models.CharField(max_length=13, verbose_name="Guess House Number")
    # Bank Details
    mobile_money = models.CharField(max_length=14,default='unavailable',)
    account_number = models.CharField(max_length=70,default='unavailable',help_text="Can also be a mobile money account")
    #Bank code for momo is MTN IF not specified
    bank_code = models.CharField(max_length=50, choices=Banks ,default='unavailable')
    
    manager = models.OneToOneField(CustomUser, on_delete=models.SET_NULL,null=True,)
    manager_contact = models.CharField(max_length=10, blank=True, verbose_name="Manager's Contact")

    address = map_fields.AddressField(max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=500, blank=True, null=True)


    verified = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = _("GuestHouse")
        verbose_name_plural = _("GuestHouses")

    def __str__(self):
        return self.guest_house_name

    def get_absolute_url(self):
        return reverse("GuestHouse_detail", kwargs={"pk": self.pk})
