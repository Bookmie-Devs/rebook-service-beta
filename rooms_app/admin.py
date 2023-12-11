from django.contrib import admin
from .models import  RoomProfile
# Register your models here.

''.capitalize
class CustomRoomAdminPanel(admin.ModelAdmin):

    fieldsets = (
        ('General', {
            "fields": ('room_no','floor_no','room_price','hostel','campus',
                       'room_capacity','bed_space_left','gender', 'rating'),}),
        
        ('Specs', {'fields':('inbuilt_kitchen','inbuilt_bathroom',
                             'inbuilt_balcony','air_condition',)}),

        ('System Status', {'fields':('booking_occupied','platform_occupied','occupied')}),
    )
    


admin.site.register(RoomProfile, CustomRoomAdminPanel)
