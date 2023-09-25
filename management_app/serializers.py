from rest_framework import serializers
from rooms_app.models import RoomProfile
from core.models import Tenant
from core.models import Booking
from rest_framework.reverse import reverse

class RoomListSerializer(serializers.ModelSerializer):
    #gets and return the method "get_detail_view_url" into the fileds
    detail_view_url = serializers.SerializerMethodField()
    class Meta:
        model=RoomProfile
        fields =('detail_view_url','room_id','room_no','room_capacity', 'room_price','room_category', 'occupied', 'hostel')

    """Return the deatail url for the each room in the list """
    def get_detail_view_url(self, obj):
        request = self.context.get('request')

        return reverse( viewname='api_app:room-detail',
                        kwargs={'room_id':obj.room_id},
                        request=request)

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields ='__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields=('user','Room_number','Hostel', 'Room' )


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomProfile
        fields =('room_no','room_capacity', 'room_price','room_category', 'occupied', 'hostel')
