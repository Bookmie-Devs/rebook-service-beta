from collections.abc import Iterable
from random import randint
import uuid
from django.db import models
from accounts.models import CustomUser
from campus_app.models import CampusProfile
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.

def genrate_agent_code()-> str:
    code = f"BA{randint(10000, 99999)}"
    while Agent.objects.filter(agent_code=code).exists():
         code = f"BA{randint(10000, 99999)}"
    return code


class Agent(models.Model):
    agent_code = models.CharField(primary_key=True, max_length=7, editable=False, default=genrate_agent_code, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=False, unique=True)
    mobile_money = models.CharField(max_length=10, blank=False, unique=True)
    agent_profile_picture = models.ImageField(default="unknown_profile.jpg", upload_to="AgentProfilePictures")
    ghana_card = models.ImageField(default="unknown_profile.jpg", upload_to="AgentIDPictures")
    is_verified = models.BooleanField(default=False)
    is_active =  models.BooleanField(default=False)
    date_join = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")

    def __str__(self):
        return '%s || %s' % (self.agent_code, self.user.username)


class AgentSale(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    date = models.DateField(_("date recorded"), auto_now=False, auto_now_add=True)
    last_updated = models.DateField(_("last updated"), auto_now=True, auto_now_add=False)
    year = models.PositiveIntegerField(default=timezone.now().year)
    number_of_sales = models.IntegerField(default=0)

    class Meta:
        db_table = "agent_sales"