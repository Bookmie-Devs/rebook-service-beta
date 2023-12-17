from django.db import models
from django.urls import reverse
import uuid
from campus_app.models import CampusProfile
from django.utils.translation import gettext_lazy as _
from django_google_maps import fields as map_fields
from accounts.models import CustomUser

from django.db import models
from accounts.models import CustomUser
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


class Guest(models.Model):
    guest_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    phone = models.CharField(max_length=14)
    phone_code = models.CharField(max_length=10, null=True, blank=True)
    
    class Meta:
        verbose_name = _("Guest")
        verbose_name_plural = _("Guests")

    def __str__(self):
        return self.phone

    def get_absolute_url(self):
        return reverse("Guest_detail", kwargs={"pk": self.pk})


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


class GuestHouseRooms(models.Model):
    room_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    room_image = models.ImageField(upload_to='GuestHouseRoomImages',default='room_img_unavailable.jpg')
    guest_house = models.ForeignKey(GuestHouse, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=50)
    room_price = models.DecimalField(decimal_places=2)
    campus = models.ForeignKey(CampusProfile, on_delete=models.PROTECT)
    

    class Meta:
        verbose_name = _("GuestHouseRooms")
        verbose_name_plural = _("GuestHouseRoomss")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("GuestHouseRooms_detail", kwargs={"pk": self.pk})



# Guest house booking
class GuestBooking(models.Model):
    room = models.ForeignKey(GuestHouseRooms, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    guest_house = models.ForeignKey(GuestHouse, on_delete=models.CASCADE)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE)
    guest_user = models.ForeignKey(Guest, on_delete=models.CASCADE)
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
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


# Date
timing = timezone.now()
class GuestPaymentHistory(models.Model):
    payment_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    reference = models.CharField(max_length=500, unique=True, editable=False,
                                 default='unavailable')
    guest_user = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    amount = models.DecimalField(decimal_places=1, max_digits=7)
    account_payed_to = models.CharField(max_length=300)
    room = models.ForeignKey(GuestHouseRooms, on_delete=models.SET_NULL, null=True)
    hostel = models.ForeignKey(GuestHouse, on_delete=models.SET_NULL, null=True)
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
        self.reference = f'py0{timing.day}ref-{self.payment_id}-{self.user.first_name.lower()[:3]}-{self.user.student_id}-{self.user.last_name.lower()[:2]}-3369-{self.user.first_name.lower()}-0{timing.month}-{self.user.last_name.lower()}-0{timing.year}-pay-to-rbk'.replace(" ","") 
        super().save(*args, **kwargs)
    
    def amount_value(self) -> int:
        return self.amount*100