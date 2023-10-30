from typing import Any
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

notify_me =settings.EMAIL_HOST_USER,

# Notification
class NotifyMe:
    def __init__(self, subject:str ,name:str, phone:str, message:str, date: Any) -> None:
        self.name = name
        self.phone = phone
        self.message = message
        self.date = date
        self.subject=subject
    
    def notify_by_email(self) -> None:
        # data for nofification
        context = {"name": self.name,"phone":self.phone,
                   "message":self.message,"date":self.date,
                   "subject":self.subject}
        
        send_mail(from_email=notify_me, recipient_list=[notify_me], 
                  subject=self.subject, message=render_to_string(
                  template_name='emails/notify_me.html',
                  context=context),fail_silently=True
                    )
        
    def notify_by_sms(self) -> None:
        pass