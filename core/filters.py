import django_filters
from hostel_app.models import HostelProfile
from rooms_app.models import RoomProfile


class HostelFilter(django_filters.CharFilter):
    class Meta:
        model = HostelProfile
        fields = ['hostel_name']


class RoomFilters(django_filters.FilterSet):
    class Meta:
        model = RoomProfile
        fields = ['room_capacity', 'room_price', 'campus']

