from rest_framework import serializers
from rooms_app.models import RoomProfile
from core.models import Tenant
from hostel_app.models import HostelProfile
from core.models import Booking
from rest_framework.reverse import reverse

class RoomListSerializer(serializers.ModelSerializer):
    
    #gets and return the method "get_detail_view_url" into the fileds
    detail_url = serializers.SerializerMethodField( read_only=True,
                        method_name= 'get_detail_url',)
    
    number_of_tenants = serializers.SerializerMethodField(read_only=True,
                        method_name='get_number_of_tenants')
    class Meta:
        model=RoomProfile
        fields =('room_no',
                 'room_capacity',
                 'room_price',
                 'occupied',
                 'bed_space_left',
                 'number_of_tenants',
                 'detail_url',
                 'room_id',)

    #Return the deatail url for the each room in the list
    def get_detail_url(self, obj: RoomProfile):

        request = self.context.get('request')

        return reverse('management:room-details',
                        kwargs={'room_id':obj.room_id},
                        request=request,
                        )
    # count and retun the number of tenants in the room
    def get_number_of_tenants(self, obj:RoomProfile):
        no_of_tenants = Tenant.objects.filter(room=obj).count()
        return no_of_tenants

class TenantListSerializer(serializers.ModelSerializer):
    
    """method serializers"""
    # tenant name
    name = serializers.SerializerMethodField(method_name='get_tenant_name',
                                             read_only=True)
    # room number
    room_number = serializers.SerializerMethodField(read_only=True)
    # student ID
    student_id = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tenant
        fields = (
            'name',
            'room_number',
            'student_id',
            'payed',
            'checked_in',
        )

    """Serializer methods"""
    def get_tenant_name(self, obj:Tenant):
        return obj.user.username
    
    def get_room_number(self, obj:Tenant):
        return obj.room.room_no
    
    def get_student_id(self, obj:Tenant):
        return obj.user.student_id


# VERIFICATION RESPONSE
class TenantVerificationSerializer(serializers.ModelSerializer):
    """method serializers"""
    # hostel name
    hostel_name = serializers.SerializerMethodField(read_only=True)
    # checked in status
    checked_in_status = serializers.SerializerMethodField(read_only=True)
    # tenant name
    tenant_name = serializers.SerializerMethodField(read_only=True)
    # room number
    room_number = serializers.SerializerMethodField(read_only=True)
    # # student ID
    student_id = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tenant
        fields = (
            'hostel_name',
            'room_number',
            'tenant_name',
            'student_id',
            'checked_in_status',
            )
    # """Serializer methods"""
    # hostel name
    def get_hostel_name(self, obj:Tenant) -> str:
        return obj.hostel.hostel_name

    def get_tenant_name(self, obj) -> str:
        return obj.user.username
    
    def get_room_number(self, obj:Tenant):
        return obj.room.room_no
    
    def get_student_id(self, obj:Tenant):
        return obj.user.student_id
    
    # checked in status
    def get_checked_in_status(self, obj:Tenant) -> str:
        if obj.checked_in:
            return "Already Checked In"
        else:
            # change status and save it
            obj.checked_in=True
            obj.save()
            return "First Arrival"


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
                 'bed_space_left',
                 'hostel',)

    #Returns the hostel name
    def get_hostel(self, obj: RoomProfile):
        return obj.hostel.hostel_name


class HostelDetialsSerializer(serializers.ModelSerializer):

    manager = serializers.SerializerMethodField(method_name='get_managers_name')
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
        
    def get_managers_name(self, obj:HostelProfile):
        return obj.hostel_manager.username
