from django.contrib import admin
from .models import CampusProfile
# Register your models here.


class CustomCampusAdminPanel(admin.ModelAdmin):

    list_display = ('campus_name','campus_code','address')


admin.site.register(CampusProfile, CustomCampusAdminPanel)