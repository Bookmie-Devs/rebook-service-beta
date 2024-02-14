from collections.abc import Iterable
from django.db import models
from accounts.models import CustomUser, Student
from hostel_app.models import HostelProfile
from rooms_app.models import RoomProfile
import uuid
from django.conf import settings
from .payStack import update_subaccount
from django.utils import timezone

# Date
timing = timezone.now()
class PaymentHistory(models.Model):
    payment_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    reference_id = models.CharField(max_length=500, unique=True, editable=False,default='unavailable')
    paystack_reference = models.CharField(max_length=500, default='unavailable')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    account_payed_to = models.CharField(max_length=300)
    room = models.ForeignKey(RoomProfile, on_delete=models.SET_NULL, null=True)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.SET_NULL, null=True)
    successful = models.BooleanField(default=False)
    date_of_payment = models.DateTimeField(auto_now_add=True)
    is_half_payment =  models.BooleanField(default=False)
    completed_full_payment =  models.BooleanField(default=False)
    def __str__(self) -> str:
        return f'{self.user} payed on {self.date_of_payment.date()} @{self.date_of_payment.hour}:{self.date_of_payment.minute}'

    def save(self, *args, **kwargs):
        # reference for payment with datatime of payment
        """ 
        the replace methods replace all spaces with closed
        (makes sure there are no spaces to avoids reference
        errors with paystack)
        """
        self.reference_id = f'py0{timing.day}ref-{self.payment_id}-{self.user.first_name.lower()[:3]}-{self.user.student_id}-{self.user.last_name.lower()[:2]}-3369-{self.user.first_name.lower()}-0{timing.month}-{self.user.last_name.lower()}-0{timing.year}-pay-to-rbk'.replace(" ","") 
        super().save(*args, **kwargs)
    
    def get_amount_value(self) -> int:
        return self.amount*100


class PaystackSubAccount(models.Model):
    # subaccount_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    hostel = models.OneToOneField(HostelProfile,on_delete=models.CASCADE) 
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
        db_table = 'paystack_sub_accounts'

    def save(self, *args, **kwargs):
        if self.is_updating_subaccount:
            self.percentage_charge = settings.SUBACCOUNT_PERCENTAGE
            self.update_message = update_subaccount(self.subaccount_code, self.bussiness_name, self.settlement_bank, self.account_number, self.percentage_charge)
            # setting value back to default after updating
            self.is_updating_subaccount=False
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.hostel} SubAccount'