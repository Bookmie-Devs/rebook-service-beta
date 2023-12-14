from django.contrib import admin
from .models import  RoomProfile
# Register your models here.


# function to make all rooms avaialeble
def make_all_rooms_unoccupied(modeladmin, request, queryset):
    queryset.update(occupied=False)

make_all_rooms_unoccupied.short_description = "Make all selected rooms available"


class CustomRoomAdminPanel(admin.ModelAdmin):

    fieldsets = (
        ('General', {
            "fields": ('room_no','floor_no','room_price','hostel','campus',
                       'room_capacity','bed_space_left','gender', 'rating'),}),
        
        ('Specs', {'fields':('inbuilt_kitchen','inbuilt_bathroom',
                             'inbuilt_balcony','air_condition',)}),

        ('System Status', {'fields':('booking_occupied','platform_occupied','occupied')}),
    )

    list_filter = ('occupied',)

    actions = [make_all_rooms_unoccupied]

admin.site.register(RoomProfile, CustomRoomAdminPanel)
