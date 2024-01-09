from django.db import models
from django.utils import timezone
from hostel_app.models import HostelProfile
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
# Create your models here.

class SalesStatistics(models.Model):
    hostel = models.ForeignKey(HostelProfile, on_delete=models.PROTECT)
    date = models.DateField(_("date recorded"), auto_now=False, auto_now_add=True)
    last_updated = models.DateField(_("last updated"), auto_now=True, auto_now_add=False)
    year = models.PositiveIntegerField(default=timezone.now().year)
    amount_made = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = _("Sales Stat")
        verbose_name_plural = _("Sale Stats")

    def __str__(self):
        return f"{self.hostel.hostel_name} on {self.year}"


    
class Worker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hostel = models.OneToOneField(HostelProfile, on_delete=models.SET_NULL, related_name='hostels', null=True,)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}@{self.hostel.hostel_name}"