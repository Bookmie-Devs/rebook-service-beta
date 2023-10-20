from django.contrib import admin
from .models import Booking
from .models import Tenant


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

    list_filter = ('payed','checked_in',)

    list_display = ('user','room','checked_in','start_date','end_date','payed',)


admin.site.register(Booking, CustomBookingAdminPanel)

admin.site.register(Tenant, CustomTenantAdminPanel)


admin.site.site_header = "GuudNyt"
admin.site.site_title = "GuudNyt"