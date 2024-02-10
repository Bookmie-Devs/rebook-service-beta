from django.db.models.signals import post_save
from django.core.mail import send_mass_mail, send_mail
from django.conf import settings
from django.dispatch import receiver
from accounts.models import CustomUser
from .models import NewsLetterMessage, NewsletterEmails, GeneralNewsLetter

# SIGNALS TO DILIVER MESSAGE AFTER THEY HAVE BEEN SAVED

"""For sending news to subcribe users only"""
@receiver(post_save, sender=NewsLetterMessage)
def send_newsletter(sender, instance, created, **kwargs):
    recievers = []
    if created:
        for emails in NewsletterEmails.objects.all():
            recievers.append(emails.email)
            print(recievers)
            send_mail(subject=instance.subject, message=instance.message, fail_silently=True, 
                    from_email=settings.EMAIL_HOST_USER, recipient_list=recievers)    



"""General message to all users"""
@receiver(post_save, sender=GeneralNewsLetter)
def send_general_newsletter(sender, instance, created, **kwargs):
    recievers = []
    if created:
        for user in CustomUser.objects.all():
            recievers.append(user.email)
            send_mail(subject=instance.subject, message=instance.message, fail_silently=True, 
                    from_email=settings.EMAIL_HOST_USER, recipient_list=recievers)    

