from django.contrib import admin
from .models import AnonymousGuest, GuestHouse, GuestBooking, GuestHouseRoom, GuestPaymentHistory
# Register your models here.

admin.site.register(AnonymousGuest)
admin.site.register(GuestHouse)
admin.site.register(GuestBooking)
admin.site.register(GuestHouseRoom)
admin.site.register(GuestPaymentHistory)