from django.contrib import admin
from .models import AnonymousGuest, GuestHouse, GuestBooking, GuestHouseRooms, GuestPaymentHistory
# Register your models here.

admin.site.register(AnonymousGuest)
admin.site.register(GuestHouse)
admin.site.register(GuestBooking)
admin.site.register(GuestHouseRooms)
admin.site.register(GuestPaymentHistory)