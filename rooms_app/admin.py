from django.contrib import admin
from .models import  RoomProfile
from django.db.models import F
# Register your models here.

# function to make all rooms avaialeble
def make_all_rooms_unoccupied(modeladmin, request, queryset):
    # Make each room unoccupied   
    queryset.update(occupied=False,
    # And set the bed sapce left to room capacity
    bed_space_left=F('room_capacity'))

make_all_rooms_unoccupied.short_description = "Make all selected rooms available"


class CustomRoomAdminPanel(admin.ModelAdmin):

    fieldsets = (
        ('General', {
            "fields": ('room_no','floor_no','room_price','hostel','campus',
                       'room_capacity','bed_space_left','gender', 'rating'),}),
        
        ('Specs', {'fields':('inbuilt_kitchen','inbuilt_bathroom',
                             'inbuilt_balcony','air_condition',)}),

        ('System Status', {'fields':('booking_occupied','platform_occupied','accept_half_payment','occupied')}),
    )

    list_filter = ('campus', 'occupied','room_capacity','gender',)

    actions = [make_all_rooms_unoccupied]

admin.site.register(RoomProfile, CustomRoomAdminPanel)
