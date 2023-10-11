from django.db import models
from accounts.models import CustomUser
from hostel_app.models import HostelProfile
from rooms_app.models import RoomProfile
import uuid

class PaymentHistory(models.Model):
    payment_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    reference = models.CharField(max_length=500, unique=True, editable=False,
                                 default='unavailable')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    amount = models.DecimalField(decimal_places=1, max_digits=7)
    account_payed_to = models.CharField(max_length=300)
    room = models.ForeignKey(RoomProfile, on_delete=models.SET_NULL, null=True)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.SET_NULL, null=True)
    successfull = models.BooleanField(default=False)
    date_of_payment = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} payed on {self.date_of_payment.date()} @{self.date_of_payment.hour}:{self.date_of_payment.minute}'

    def save(self, *args, **kwargs):
        
        # reference for payment with datatime of payment
        self.reference = f'pay-{self.payment_id}-{self.user.first_name.upper()}-{self.user.student_id}-{self.user.last_name.upper()}'
        super().save(*args, **kwargs)
    
    def amount_value(self) -> int:
        return self.amount*100


class PaystackSubAccount(models.Model):
    hostel = models.OneToOneField(HostelProfile,on_delete=models.CASCADE) 
    bussiness_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=30)
    subaccount_code = models.CharField(max_length=50, 
                                       default="unavailable",
                                       unique=True)
    bank_code = models.CharField(max_length=50, default="unavailable")
    settlement_bank = models.CharField(max_length=80, default="unavailable")
    percentage_charge = models.DecimalField(max_digits=5, 
                                            decimal_places=2,
                                            default=0)
    account_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'paystack_sub_accounts'


    def __str__(self) -> str:
        return f'{self.hostel} SubAccount'