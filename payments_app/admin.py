from django.contrib import admin
from .models import PaymentHistory, PaystackSubAccount, PhysicalPaymentHistory

# Register your models here.
def update_hostel_percentage_charge(modeladmin, request, queryset:PaystackSubAccount):
    queryset.update()

class CustomPaystackSubAccountAdminPanel(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            "fields": (
                'hostel','bussiness_name','account_number','subaccount_code','primary_contact_name','bank_code',
                'settlement_bank','percentage_charge','account_verified',
            ),
        }),
        ('Use This Section When Updating Subaccount',{'fields':('is_updating_subaccount','update_message',)})
    )
    
    search_fields = ('subaccount_code',)

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
        'student', 'amount',
        # 'access_code_used',
        'successful','date_of_payment',
    )

class PhysicalPaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'reference', 'successful')

admin.site.register(PhysicalPaymentHistory, PhysicalPaymentAdmin)

admin.site.register(PaymentHistory, CustomPaymentsAdminPanel)

admin.site.register(PaystackSubAccount, CustomPaystackSubAccountAdminPanel)