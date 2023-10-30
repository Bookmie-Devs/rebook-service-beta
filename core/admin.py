from django.contrib import admin
from .models import Booking
from .models import Tenant
# from .filters import IsActiveFilter


class CustomBookingAdminPanel(admin.ModelAdmin):

    search_fields = ['user']

    # list_filter = ('payed','hostel',)

    list_display = ('user','room','start_time','end_time','payed',)


class CustomTenantAdminPanel(admin.ModelAdmin):

    fieldsets = (('DO NOT EDIT OR SAVE ANY INSTANCE HERE',{"fields":(
        'user',
        'room',
        'hostel',
        'payed',
        'checked_in',
    )}),)

  
    search_fields = ('user',)

    list_filter = ('payed','checked_in','end_date',)

    list_display = ('user','room','checked_in','start_date','end_date','payed','is_active_display',)

    # display if user vcode is active
    def is_active_display(self, obj):
        return obj.is_active()
    is_active_display.boolean = True
    is_active_display.short_description = 'Is Active'


admin.site.register(Booking, CustomBookingAdminPanel)

admin.site.register(Tenant, CustomTenantAdminPanel)


admin.site.site_header = "GuudNyt"
admin.site.site_title = "GuudNyt"