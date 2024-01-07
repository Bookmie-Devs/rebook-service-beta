from rest_framework import serializers
from rooms_app.models import RoomProfile
from core.models import Tenant
from hostel_app.models import HostelProfile
from django.utils import timezone
from core.models import Booking
from rest_framework.reverse import reverse
from .models import SalesStatistics

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
        return reverse('management:room-details',kwargs={'room_id':obj.room_id},
                        request=request,)
    
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

    phone = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tenant
        fields = (
            'name',
            'room_number',
            'student_id',
            'payed',
            'checked_in',
            'phone',
        )

    """Serializer methods"""
    def get_tenant_name(self, obj:Tenant):
        return obj.user.username
    
    def get_phone(self, obj:Tenant) -> str:
        return obj.user.phone
    
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
    # statistics
    total_sales = serializers.SerializerMethodField(read_only=True)
    number_of_rooms = serializers.SerializerMethodField(read_only=True)
    number_of_tenants = serializers.SerializerMethodField(read_only=True)
    number_rooms_occupied = serializers.SerializerMethodField(read_only=True)
    number_of_4_in_a_room = serializers.SerializerMethodField(read_only=True)
    number_of_3_in_a_room = serializers.SerializerMethodField(read_only=True)
    number_of_2_in_a_room = serializers.SerializerMethodField(read_only=True)
    number_of_1_in_a_room = serializers.SerializerMethodField(read_only=True)
    total_bed_space_left = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HostelProfile
        fields = ('hostel_name',
                  'manager',
                  'hostel_manager_profile_picture',
                  'hostel_image',
                  'facilities',
                  'manager_contact',
                  'hostel_contact','other_contact',
                  'mobile_money',
                  'hostel_email',
                  'price_range',
                  'main_website',
                  'location',
                  
                #  statistics
                  'number_of_rooms',
                  'number_of_tenants',
                  'number_rooms_occupied',
                  'total_sales',
                  'total_bed_space_left',
                  'number_of_4_in_a_room',
                  'number_of_3_in_a_room',
                  'number_of_2_in_a_room',
                  'number_of_1_in_a_room',
                  )
        
    def get_managers_name(self, obj:HostelProfile):
        return obj.hostel_manager.username
    
    # STATISTICS
    def get_number_of_rooms(self, obj:HostelProfile):
        # request = self.context.get('request')
        room_count = RoomProfile.objects.filter(hostel=obj).count()
        return room_count

    def get_total_bed_space_left(self, obj:HostelProfile):
        total_bed_space_left: int = 0
        rooms = RoomProfile.objects.filter(hostel=obj)
        for room in rooms:
            # add bed spaces
            total_bed_space_left = total_bed_space_left + room.bed_space_left
        # return value
        return total_bed_space_left

    def get_total_sales(self, obj:HostelProfile):
        total_sales: float = 0
        active_tenants = Tenant.objects.filter(hostel=obj, end_date__gt=timezone.now())
        for tenant in active_tenants:
            # get total amount each user paid for the room
            total_amount = total_sales + float(tenant.room.room_price) 
            total_sales = float(total_amount)
        # return value
        return total_sales

    def get_number_of_tenants(self, obj:HostelProfile):
        # tenants whoose end_date is greater than current date
        tenant_count = Tenant.objects.filter(hostel=obj,end_date__gt=timezone.now()).count()
        return tenant_count
    
    def get_number_rooms_occupied(self, obj:HostelProfile):
        room_occupied_count = RoomProfile.objects.filter(hostel=obj,occupied=True).count()
        return room_occupied_count

    def get_number_of_4_in_a_room(self, obj:HostelProfile):
        number_of_4_in_a_room = RoomProfile.objects.filter(hostel=obj,room_capacity=4).count()
        return number_of_4_in_a_room
    
    def get_number_of_3_in_a_room(self, obj:HostelProfile):
        number_of_3_in_a_room = RoomProfile.objects.filter(hostel=obj,room_capacity=3).count()
        return number_of_3_in_a_room
    
    def get_number_of_2_in_a_room(self, obj:HostelProfile):
        number_of_2_in_a_room = RoomProfile.objects.filter(hostel=obj,room_capacity=2).count()
        return number_of_2_in_a_room
    
    def get_number_of_1_in_a_room(self, obj:HostelProfile):
        number_of_1_in_a_room = RoomProfile.objects.filter(hostel=obj,room_capacity=1).count()
        return number_of_1_in_a_room
    
    
class SalesStatSerializer(serializers.ModelSerializer):
    amount= serializers.SerializerMethodField(read_only=True, method_name='amount_in_float')
    class Meta:
        model = SalesStatistics
        fields = (
            'year',  
            'amount',
        )
    def amount_in_float(self, obj: SalesStatistics):
        return float(obj.amount_made)
    