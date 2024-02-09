from collections.abc import Iterable
import uuid
from django.db import models
from accounts.models import CustomUser
from campus_app.models import CampusProfile
from django.utils.translation import gettext_lazy as _
# Create your models here.

class HostelAgent(models.Model):
    agent_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    agent_code = models.CharField(max_length=10, editable=False, unique=True ,blank=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    campus_affiliation =  models.OneToOneField(CampusProfile, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=False, unique=True)
    mobile_money = models.CharField(max_length=10, blank=False)
    agent_profile_picture = models.ImageField(default="unknown_profile.jpg", upload_to="AgentsProfilePictures")
    is_verified = models.BooleanField(default=False)
    is_active =  models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Hostel Agent")
        verbose_name_plural = _("Hostel Agents")

    def save(self, *args, **kwargs) -> None:
        self.agent_code = f"{self.user.first_name[:2]}{self.user.last_name[:2]}-{str(self.agent_id)[:4]}-{self.user.first_name[:2]}-0912"
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("HostelAgent_detail", kwargs={"pk": self.pk})