from django.contrib import admin
from .models import HostelProfile
# from django_google_maps import widgets as map_widgets
# from django_google_maps import fields as map_fields


class CustomHostelAdminPanel(admin.ModelAdmin):

    fieldsets = (
        ('General', {"fields":('hostel_name',
                          'hostel_image',
                          'category',
                          'rating',
                          'price_range','hostel_motto',
                          'number_of_rooms',
                          'hostel_campus','hostel_manager',)}),

        ('Contact Details', {'fields':('hostel_email',
                                       'hostel_contact',
                                       'location',
                                    'main_website',
                                    )},),     
  
        ('Bank Details', {"fields":('mobile_money','account_number',
                                    'bank_code',)}),

        ('verification', {"fields": ('verified',)}),

        #forbid
        ('Forbbiden',{'fields':('hostel_code',)}),
    )

    search_fields = ('hostel_name','hostel_code')

    list_display = ('hostel_name','hostel_code','hostel_manager','hostel_contact','verified',)


admin.site.register(HostelProfile, CustomHostelAdminPanel)

