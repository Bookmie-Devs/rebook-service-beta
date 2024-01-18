from django.contrib import admin
from .models import PaymentHistory, PaystackSubAccount

# Register your models here.
def update_hostel_percentage_charge(modeladmin, request, queryset:PaystackSubAccount):
    queryset.update()

class CustomPaystackSubAccountAdminPanel(admin.ModelAdmin):

    search_fields = ('hostel','subaccount_code')

    list_display = ('bussiness_name','subaccount_code',
                    'settlement_bank','bank_code',
                    'percentage_charge',
                    'account_verified',)
    
    
# customize payment history admin panel
class CustomPaymentsAdminPanel(admin.ModelAdmin):

    list_filter = (
        'successful', 'date_of_payment',
    )

    list_display = (
        'user', 'amount',
        # 'access_code_used',
        'successful','date_of_payment',
    )

admin.site.register(PaymentHistory, CustomPaymentsAdminPanel)

admin.site.register(PaystackSubAccount, CustomPaystackSubAccountAdminPanel)