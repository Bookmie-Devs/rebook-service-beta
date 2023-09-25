from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User
from datetime import datetime
from accounts.models import StudentProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user = instance, campus=instance.campus, 
        user_phone=instance.phone)
        instance.save()


