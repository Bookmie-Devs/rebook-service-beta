from django.contrib import admin
from .models import AnonymousGuest, GuestHouse, GuestBooking, GuestHouseRoom, GuestHouseManager ,PaystackGuestHouseSubAccount,GuestPaymentHistory
from django_google_maps import fields as map_fields
from django_google_maps import widgets as map_widgets
#  Register your models here.


class CustomGuestHouseAdmin(admin.ModelAdmin):


    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

admin.site.register(AnonymousGuest)
admin.site.register(PaystackGuestHouseSubAccount)
admin.site.register(GuestHouse, CustomGuestHouseAdmin)
admin.site.register(GuestBooking)
admin.site.register(GuestHouseRoom)
admin.site.register(GuestPaymentHistory)
admin.site.register(GuestHouseManager)