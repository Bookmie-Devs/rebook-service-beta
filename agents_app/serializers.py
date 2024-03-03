from django.http import HttpRequest
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from rooms_app.models import RoomProfile
from .models import Agent
from hostel_app.models import HostelProfile

class AgenProfilesSerilizer(ModelSerializer):
    class Meta:
        model = Agent
        fields ='__all__'

class AgentHostelListSerializer(ModelSerializer):
    class Meta:
        model = HostelProfile
        fields = ('hostel_name', 'hostel_code', 'hostel_image', 'verified' )


class AgentHostelProfileSerializer(ModelSerializer):
    class Meta:
        model = HostelProfile
        fields = ('hostel_code' ,'hostel_name', 'number_of_rooms' ,'hostel_image', 'address', 'hostel_contact', )


class RoomListSerializer(ModelSerializer):
    hostel_name = SerializerMethodField(read_only=True)
    class Meta:
        model = RoomProfile
        fields = ('hostel_name', 'room_no', 'bed_space_left' ,'occupied', 'verified','room_id',)

    def get_hostel_name(self, obj:RoomProfile):
        return obj.hostel.hostel_name

class RoomProfileSerializer(ModelSerializer):
    class Meta:
        model = RoomProfile
        fields = ('bed_space_left' ,'occupied',)


class AgentRoomsSerializer(ModelSerializer):
    hostel = SerializerMethodField(read_only=True)
    class Meta:
        model = RoomProfile
        fields = ('room_no', 'hostel' ,'room_id', )

    
    def get_hostel(self, obj: RoomProfile):
        return obj.hostel.hostel_name


class HostelCreationSerializer(ModelSerializer):
    class Meta:
        model = HostelProfile
        fields = ('hostel_name',
                  'hostel_contact',
                  'other_contact',
                  'bank_code',
                  'account_number',
                  'number_of_rooms',
                  'campus',
                  'agent_affiliate',
                  'hostel_image', 
                  'hostel_image2', 
                  'hostel_image3',
                  'hostel_image4', 
                  'hostel_image5',
                  'room_image',
                  'room_image2',
                  'room_image3',
                  'room_image4',
                  'room_image5',
                  'room_image6',
                  'address',
                  'location',
                  'geolocation',)


    