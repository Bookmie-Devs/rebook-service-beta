from django.contrib import admin
from .models import PaymentHistory, PaystackSubAccount

# Register your models here.

class CustomPaystackSubAccountAdminPanel(admin.ModelAdmin):

    search_fields = ('hostel','subaccount_code')

    list_display = ('bussiness_name','subaccount_code',
                    'settlement_bank','bank_code',
                    'percentage_charge',
                    'account_verified',)
    
class CustomPaymentsAdminPanel(admin.ModelAdmin):

    list_display = (
        'user', 'amount', 'successful','date_of_payment',
    )

admin.site.register(PaymentHistory)

admin.site.register(PaystackSubAccount, CustomPaystackSubAccountAdminPanel)