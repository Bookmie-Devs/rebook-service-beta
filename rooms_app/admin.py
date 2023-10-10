from django.contrib import admin
from .models import  RoomProfile
# Register your models here.


class CustomRoomAdminPanel(admin.ModelAdmin):

    fieldsets = (
        ('General', {
            "fields": ('room_no', 'floor_no','room_price','hostel','campus',
                       'room_capacity','room_img', 'rating'),}),
        
        ('Specs', {'fields':('contains_kitchen','shared_kitchen',
                             'contains_bathroom','air_condition')}),

        ('Status', {'fields':('booking_occupied', 'occupied')}),
    )
    


admin.site.register(RoomProfile, CustomRoomAdminPanel)
