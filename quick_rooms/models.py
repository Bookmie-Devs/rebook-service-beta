from django.conf import settings
from django.db import models

# Create your models here.
from accounts.models import CustomUser
from collections.abc import Iterable
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from guesthouses.models import GuestHouse, GuestHouseRooms
from uuid import uuid4

from campus_app.models import CampusProfile
from payments_app.payStack import update_subaccount
# Create your models here.

class AnonymousGuest(models.Model):
    quest_id = models.UUIDField(_("guest id"), default=uuid4,editable=False, unique=True)
    phone = models.CharField(_("phone number"), max_length=15)
    quest_code = models.CharField(_("anonymous code"), max_length=10, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    code_life_time = models.TimeField(_("code life time"),auto_now=False,auto_now_add=False,blank=True,null=True)

    def save(self, *args, **kwargs) -> None:
        from random import randint
        code = randint(100000,900000)
        while AnonymousGuest.objects.filter(quest_code=code).exists():
            code = randint(100000, 900000)
        self.quest_code=code
        self.code_life_time = timezone.now() + timezone.timedelta(minutes=10)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.phone
    
    

from django.db import models
from django.urls import reverse
import uuid
# from campus_app.models import CampusProfile
from django.utils.translation import gettext_lazy as _
from django_google_maps import fields as map_fields
# from accounts.models import CustomUser

from django.db import models
import uuid
from django.utils import timezone

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
    name = models.CharField(max_length=100, verbose_name="Name")
    house_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    house_code = models.CharField(max_length=10,null=True, blank=True,unique=True)
    house_image = models.ImageField(upload_to='GuestHouseImage',default='unavailable.jpg')
    campus = models.ForeignKey(CampusProfile, on_delete=models.PROTECT)
    phone = models.CharField(max_length=13, verbose_name="Guess House Number")
    # Bank Details
    mobile_money = models.CharField(max_length=14,default='unavailable',)
    account_number = models.CharField(max_length=70,default='unavailable',help_text="Can also be a mobile money account")
    #Bank code for momo is MTN IF not specified
    bank_code = models.CharField(max_length=50, choices=Banks ,default='unavailable')
    
    # manager = models.OneToOneField(CustomUser, on_delete=models.SET_NULL,null=True,)
    manager_contact = models.CharField(max_length=10, blank=True, verbose_name="Manager's Contact")

    location =models.CharField(max_length=10, verbose_name="Main location") 
    manager = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    address = map_fields.AddressField(max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=500, blank=True, null=True)


    verified = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = _("Motel/GuestHouse")
        verbose_name_plural = _("Motels/GuestHouses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("GuestHouse_detail", kwargs={"pk": self.pk})


class GuestHouseRoom(models.Model):
    room_name = models.CharField(max_length=50, default='unavailable')
    room_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    guest_house = models.ForeignKey(GuestHouse, on_delete=models.CASCADE)
    room_image = models.ImageField(upload_to="GuestHouse", default='unavailable.jpg')
    room_image1 = models.ImageField(upload_to="GuestHouse", default='unavailable.jpg')
    room_image2 = models.ImageField(upload_to="GuestHouse", default='unavailable.jpg')
    room_image3 = models.ImageField(upload_to="GuestHouse", default='unavailable.jpg')
    room_price = models.DecimalField(decimal_places=2, max_digits=10,)
    previous_price_check = models.DecimalField(blank=True, editable=False,
                                      null=True, decimal_places=2, max_digits=7)
    ptf_room_price = models.DecimalField(default=0.0, editable=False, decimal_places=2, max_digits=8)
    campus = models.ForeignKey(CampusProfile, on_delete=models.SET_NULL,
                                verbose_name="Campus where Room is located",
                                null=True)
    occupied = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("GuestHouseRoom")
        verbose_name_plural = _("GuestHouseRooms")

    def __str__(self):
        return self.room_name
    
    def save(self, *args, **kwargs) -> None:
            # CHECK IF ROOM PRICE IS SAME A PREVIOUS PRICE IF NOT UPDATE FIELDS
        # Without this check, anytime the save method is called the pft_room_price will
        # and upadte itself.
        if self.room_price!=self.previous_price_check:
            addtional_pricing: float = float(self.room_price) * settings.SUPPLY_COST_PERCENTAGE
            # additional price for half payment
            addtional_half_pricing: float = float(self.room_price/2) * settings.SUPPLY_COST_PERCENTAGE
            # new prices
            self.ptf_room_price = float(self.room_price) + addtional_pricing
            self.half_pricing = float(self.room_price/2) + addtional_half_pricing
            # equate the two to maintain the balance
            self.previous_price_check = self.room_price
        else:
            """
            Do nothing to ptf price if room price is still the same,
            could be that the room has been updated but not the 
            price which does not need to be updated
            """
            pass
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("GuestHouseRoom_detail", kwargs={"pk": self.pk})


# Guest house booking
class GuestBooking(models.Model):
    room = models.ForeignKey(GuestHouseRoom, on_delete=models.CASCADE)
    guest_house = models.ForeignKey(GuestHouse, on_delete=models.CASCADE)
    campus = models.ForeignKey(CampusProfile, on_delete=models.PROTECT, null=True)
    guest_user = models.ForeignKey(AnonymousGuest, on_delete=models.CASCADE)
    booking_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)
    payed = models.BooleanField(default=False) 
    class Meta:
        ordering = ('-start_time',)

    def delete_if_not__valid(self):
        query = GuestBooking.objects.get(booking_id=self.booking_id)
        query.delete()
    
    # def save(self, *args, **kwargs):
    #     """
    #     using timezone.now() instead of start_time because
    #     start usese auto_now_add which is NoneType until the
    #     the data is saved to the database
    #     """
    #     self.end_time = (timezone.now() + timedelta(minutes=60))
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} || {self.room}'


class PaystackGuestHouseSubAccount(models.Model):
    # subaccount_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    guest_house = models.OneToOneField(GuestHouse,on_delete=models.CASCADE) 
    bussiness_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    subaccount_code = models.CharField(max_length=50, 
                                       default="unavailable",
                                       unique=True)
    primary_contact_name = models.CharField(max_length=30, default="unavailable")
    bank_code = models.CharField(max_length=50, default="unavailable")
    settlement_bank = models.CharField(max_length=80, default="unavailable")
    percentage_charge = models.DecimalField(max_digits=5, 
                                            decimal_places=3,
                                            verbose_name="percentage charge %",
                                            default=0)
    account_verified = models.BooleanField(default=False)
    # check field when you want to update field
    is_updating_subaccount = models.BooleanField(default=False)
    update_message = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'paystack_guesthouse_sub_accounts'

    def save(self, *args, **kwargs):
        if self.is_updating_subaccount:
            self.percentage_charge = settings.SUBACCOUNT_PERCENTAGE
            self.update_message = update_subaccount(self.subaccount_code, self.bussiness_name, self.settlement_bank, self.account_number, self.percentage_charge)
            # setting value back to default after updating
            self.is_updating_subaccount=False
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.hostel} SubAccount'

# Date
timing = timezone.now()
class GuestPaymentHistory(models.Model):
    booking = models.OneToOneField(GuestBooking, on_delete=models.CASCADE, null=True)
    payment_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)
    reference_id = models.CharField(max_length=500, unique=True, editable=False,default='unavailable')
    email = models.EmailField(default="bookmie.com@gmail.com")
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    account_payed_to = models.CharField(max_length=300)
    successful = models.BooleanField(default=False)
    date_of_payment = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} payed on {self.date_of_payment.date()} @{self.date_of_payment.hour}:{self.date_of_payment.minute}'

    def save(self, *args, **kwargs):
        # reference for payment with datatime of payment
        """ 
        the replace methods replace all spaces with closed
        (makes sure there are no spaces to avoids reference
        errors with paystack) 
        """
        self.reference_id = f'py0{timing.day}ref-{self.payment_id}-3369-0{timing.month}-0{timing.year}-pay-to-rbk'.replace(" ","") 
        super().save(*args, **kwargs)
    
    def amount_value(self) -> int:
        return self.amount*100