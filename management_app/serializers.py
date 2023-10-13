from rest_framework import serializers
from rooms_app.models import RoomProfile
from core.models import Tenant
from hostel_app.models import HostelProfile
from core.models import Booking
from rest_framework.reverse import reverse

class RoomListSerializer(serializers.ModelSerializer):
    #gets and return the method "get_detail_view_url" into the fileds
    detail_url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=RoomProfile
        fields =('room_no',
                 'room_capacity',
                 'room_price',
                 'occupied',
                 'detail_url')

    #Return the deatail url for the each room in the list
    def get_detail_url(self, obj):

        request = self.context.get('request')
        
        return reverse('management:room-details',
                        request=request,
                        kwargs={'room_id':obj.room_id})

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields ='__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields=('user','room_number','hostel', 'room' )


class RoomDetailSerializer(serializers.ModelSerializer):
    hostel = serializers.SerializerMethodField()
    class Meta:
        model = RoomProfile
        fields =('room_no',
                 'room_capacity', 
                 'room_price',
                 'occupied',
                 'hostel')

    #Returns the hostel name
    def get_hostel(self, obj):
        return obj.hostel.hostel_name


class HostelDetialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelProfile
        fields = ('hostel_name',
                  'mangers_contact',
                  'hostel_image',
                  'phone','other_phone',
                  'bank_details',
                  'mobile_money',
                  'hostel_email',
                  'price_range',
                  'hostel_main_site',
                  'address',)
