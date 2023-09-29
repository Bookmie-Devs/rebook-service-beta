from django.contrib import admin
from .models import PaymentHistory, PaystackSubAccount

# Register your models here.

admin.site.register(PaymentHistory)

admin.site.register(PaystackSubAccount)