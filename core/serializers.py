from rest_framework import serializers
from hostel_app.models import HostelProfile
from django.urls import reverse
from core.models import Booking, Tenant

class HostellistSerializer(serializers.ModelSerializer):
    
    # gets and return the method "get_absolute_view_url" into the fileds
    absolute_url = serializers.SerializerMethodField(
                        method_name= 'get_absolute_url',
                        read_only=True)
    class Meta:
        model=HostelProfile
        fields =('hostel_name',
                 'hostel_image',
                 'category',
                 'location',
                 'price_range',
                 'absolute_url',
                 'hostel_id',
                 )

    # Return the deatail url for the each room in the list
    def get_absolute_url(self, obj):
        return reverse('hostels:api-hostel-profile',
                        kwargs={'hostel_id':obj.hostel_id},
                        )
    

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class TenantSerializer(serializers.ModelSerializer):
    hostel_name = serializers.SerializerMethodField(read_only=True)
    room_number = serializers.SerializerMethodField(read_only=True)
    floor_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tenant
        filds = ('user','hostel_name','room_number','floor_number','end_date')

    def get_room_number(self, obj:Tenant):
        return obj.room.room_no
    
    def get_hostel_name(self, obj:Tenant):
        return obj.hostel.hostel_name
    
    def get_floor_number(self, obj:Tenant):
        return obj.room.floor_no
        