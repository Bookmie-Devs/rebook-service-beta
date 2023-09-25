from django.db import models
from accounts.models import CustomUser
from hostel_app.models import HostelProfile
from rooms_app.models import RoomProfile
import uuid
import secrets

class PaymentHistory(models.Model):
    # payment_id = models.UUIDField(unique=True, editable=False,primary_key=True, default=uuid.uuid4 )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    amount = models.DecimalField(decimal_places=1, max_digits=7)
    reference = models.CharField(max_length=500)
    account_payed_to = models.CharField(max_length=500)
    room = models.ForeignKey(RoomProfile, on_delete=models.SET_NULL, null=True)
    hostel = models.ForeignKey(HostelProfile, on_delete=models.SET_NULL, null=True)
    successfull = models.BooleanField(default=False)
    date_of_payment = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} payed on {self.date_of_payment.date()} @{self.date_of_payment.hour}:{self.date_of_payment.minute}'

    def save(self, *args, **kwargs):
        while not self.reference:
            reference = secrets.token_urlsafe(407)
            there_exits_same_ref=PaymentHistory.objects.filter(reference=reference)
            if not there_exits_same_ref:
                self.reference=reference
        super().save(*args, **kwargs)
    
    def amount_value(self) -> int:
        return self.amount*100