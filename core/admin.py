from django.contrib import admin
from .models import Booking
from .models import Tenant

admin.site.register(Booking)
admin.site.register(Tenant)

admin.site.site_header = "GuudNyt"
admin.site.site_title = "GuudNyt"