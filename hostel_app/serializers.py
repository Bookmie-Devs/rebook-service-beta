from .models import HostelProfile
from rooms_app.models import RoomProfile
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField)


class HostelProfileSerializer(ModelSerializer):

    manager = SerializerMethodField(method_name='get_managers_name')
    class Meta:
        model = HostelProfile
        fields = ('hostel_name',
                  'manager',
                  'manager_contact',
                  'hostel_contact','other_phone',
                  'mobile_money',
                  'hostel_email',
                  'price_range',
                  'main_website',
                  'location',)
        
    def get_managers_name(self, obj):
        return obj.hostel_manager.username
    

class HostelRoomsSerializer(ModelSerializer):
     class Meta:
         model = RoomProfile
         fields = (
             'room_no',
             'room_price',
             'room_capacity',
         )
