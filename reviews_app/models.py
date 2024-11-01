from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from hostel_app.models import HostelProfile
from rooms_app.models import RoomProfile


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")

    def __str__(self):
        return self.question



# feedback model
class FeedBackMessage(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    issue_resolved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}({self.phone})"


# customer care model
class CustomerCare(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    problem = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    issue_resolved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}({self.phone})"


class RecomendationFeedBacks(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="Clients", height_field=None, width_field=None, max_length=None)
    reccomendation = models.TextField()

    class Meta:
        verbose_name = _("RecomendationFeedBacks")
        verbose_name_plural = _("RecomendationFeedBacks")

    def __str__(self):
        return self.name
    

class HostelLike(models.Model):
    hostel = models.ForeignKey(HostelProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)



class GeneralNewsLetter(models.Model):
    subject = models.TextField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date
