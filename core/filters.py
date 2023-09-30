import django_filters
from django_filters import (RangeFilter, 
                            NumberFilter)
from hostel_app.models import HostelProfile
from rooms_app.models import RoomProfile


class HostelFilter(django_filters.CharFilter):
    class Meta:
        model = HostelProfile
        fields = ['hostel_name']


class RoomFilters(django_filters.FilterSet):

    """Capacity range"""
    room_capacity = NumberFilter(field_name='room_capacity')

    """Filter for room by Price"""
    room_price = RangeFilter(field_name='room_price') 
    class Meta:
        model = RoomProfile
        fields = ['room_price', 'room_capacity']

































