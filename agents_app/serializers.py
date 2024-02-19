from rest_framework.serializers import ModelSerializer, SerializerMethodField

from rooms_app.models import RoomProfile
from .models import HostelAgent
from hostel_app.models import HostelProfile

class AgenProfilesSerilizer(ModelSerializer):
    class Meta:
        model = HostelAgent
        fields ='__all__'

class AgentHostelListSerializer(ModelSerializer):
    class Meta:
        model = HostelProfile
        fields = ('hostel_name', 'hostel_code', 'hostel_image', 'verified' ,'hostel_id')


class AgentHostelSerializer(ModelSerializer):
    class Meta:
        model = HostelProfile
        fields = ('hostel_id', 'hostel_code' ,'hostel_name', 'number_of_rooms' ,'hostel_image', 'address', 'hostel_contact', )




class AgentRoomsSerializer(ModelSerializer):
    hostel = SerializerMethodField(read_only=True)
    class Meta:
        model = RoomProfile
        fields = ('room_no', 'hostel' ,'room_id', )

    
    def get_hostel(self, obj: RoomProfile):
        return obj.hostel.hostel_name