from django.contrib import admin
from .models import HostelProfile
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields


class CustomHostelAdminPanel(admin.ModelAdmin):

    fieldsets = (
        ('General', {"fields":('hostel_name',
                          'hostel_image',
                          'room_image',
                          'category',
                          'rating',
                          'price_range',
                          'number_of_rooms',
                          'campus','hostel_manager',
                          )}),

        ('Location',{"fields":('location','address','geolocation')}),

        ('Contact Details', {'fields':('hostel_email',
                                       'hostel_contact',
                                       'other_contact',
                                    'main_website',
                                    )},),     
  
        ('Bank Details', {"fields":('mobile_money','account_number',
                                    'bank_code',)}),

        (("Hostel Manager Profile"), {"fields": ("hostel_manager_profile_picture",)}),

        ('verification', {"fields": ('verified',)}),

        ('Facilities',{"fields":('facilities',),}),
        #forbid
        ('Forbbiden',{'fields':('hostel_code',)}),
    )

    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }
    search_fields = ('hostel_name','hostel_code')

    list_display = ('hostel_name','hostel_code','hostel_manager','hostel_contact','verified',)


admin.site.register(HostelProfile, CustomHostelAdminPanel)

