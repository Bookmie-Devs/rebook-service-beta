from django.contrib import admin
from .models import  RoomProfile
# Register your models here.


class CustomRoomAdminPanel(admin.ModelAdmin):

    fieldsets = (
        ('General', {
            "fields": ('room_no', 'floor_no','room_price','hostel','campus',
                       'room_capacity','bed_space_left','room_img', 'rating'),}),
        
        ('Specs', {'fields':('inbuilt_kitchen','inbuilt_bathroom',
                             'inbuilt_balconi','air_condition',)}),

        ('Status', {'fields':('booking_occupied', 'occupied')}),
    )
    


admin.site.register(RoomProfile, CustomRoomAdminPanel)
