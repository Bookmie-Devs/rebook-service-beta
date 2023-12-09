import django_filters
from django_filters import (RangeFilter, 
                            NumberFilter,
                            BooleanFilter,
                            ChoiceFilter,)
from hostel_app.models import HostelProfile
from rooms_app.models import RoomProfile
from django.contrib import admin
from django.db import models
from django.utils import timezone

class HostelFilter(django_filters.CharFilter):
    class Meta:
        model = HostelProfile
        fields = ['hostel_name']


class RoomFilters(django_filters.FilterSet):

    # gender of room
    gender = ChoiceFilter(choices=[('female','female'),('male','male')])

    """Capacity range"""
    room_capacity = NumberFilter(field_name='room_capacity')

    """Filter for room by Price"""
    ptf_room_price = RangeFilter(field_name='ptf_room_price') 
    
    class Meta:
        model = RoomProfile
        fields = ['ptf_room_price', 'room_capacity', 'gender',]




import django_filters

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        # model = Product
        fields = ['name', 'category', 'price']  # Define the fields you want to filter on


# from django.contrib import admin
# from .models import Tenant

# from django.contrib import admin
# from .models import Tenant

# class TenantAdmin(admin.ModelAdmin):
#     list_display = ('user', 'room', 'hostel', 'payed', 'checked_in', 'start_date', 'end_date', 'is_active_display')
#     actions = ['mark_as_active', 'mark_as_inactive']

#     def is_active_display(self, obj):
#         return obj.is_active()
#     is_active_display.boolean = True
#     is_active_display.short_description = 'Is Active'






























