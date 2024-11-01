from django.contrib import admin
from .models import CampusProfile, CollegeProfile
from django_google_maps import fields as map_fields
from django_google_maps import widgets as map_widgets
# Register your models here.


class CustomCampusAdminPanel(admin.ModelAdmin):

    list_display = ('campus_name','campus_code','address')

    fieldsets = (
        ('General', {
            "fields": (
                'campus_name','alias_name','campus_code','flag',
            ),
        }),
        ('Location', {'fields': ('location','address','geolocation',)}),
        ('Verifications',{'fields':('available_on_campus','end_of_acadamic_year',)}),
    )
    

    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }


class CustomCollegeAdminPanel(admin.ModelAdmin):
    list_display = ("campus","college_name","college_code",)

    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }


admin.site.register(CollegeProfile, CustomCollegeAdminPanel)

admin.site.register(CampusProfile, CustomCampusAdminPanel)