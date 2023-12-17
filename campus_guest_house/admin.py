from django.contrib import admin
from .models import GuestHouse
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
# Register your models here.


class GuestHouseAdminPanel(admin.ModelAdmin):
    list_display = ('guest_house_name','campus',)

    search_fields = ('guest_house_name',)

    fieldsets = (
        (None, {
            "fields": (
                'guest_house_name',
                'campus',
                'phone',
                'manager',
                'manager_contact',
            ),
        }),
        ("Bank Details",{
            'fields':(
                'account_number',
            )
        }),
        ("Location",{"fields":
                     ('address',
                      'geolocation',)})

    )
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

admin.site.register(GuestHouse, GuestHouseAdminPanel)