from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from .serializers import (RoomListSerializer,
                          RoomDetailSerializer,
                          HostelDetialsSerializer)

from core.models import Booking
from .serializers import TenantSerializer
from .serializers import BookingSerializer
from core.models import Tenant
from rest_framework import status
from hostel_app.models import HostelProfile
from rest_framework.permissions import (IsAuthenticated, 
                                        DjangoModelPermissions)
from rest_framework.decorators import permission_classes
from rooms_app.models import RoomProfile
from django.db.models import Q
from rest_framework import generics


@api_view(['POST'])
@permission_classes([IsAuthenticated, DjangoModelPermissions])    
def get_rooms(request):

    """Gets a list of all rooms related to 
    a particular hostel after getting the hostel code from the person who logs in"""

    try:
        if request.method == 'POST':
            hostel_code = request.data.get('hostel_code')
            get_hostel=HostelProfile.objects.get(hostel_code=hostel_code)
            get_rooms = RoomProfile.objects.filter(hostel=get_hostel)
            serializer = RoomListSerializer(get_rooms, many=True)
            return Response(serializer.data)
        
    except HostelProfile.DoesNotExist:
        return Response({'detail':'Hostel Does not exist'}, status=status.HTTP_404_NOT_FOUND)

class RoomDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = RoomDetailSerializer
    queryset = RoomProfile
    lookup_field = "room_id"
    permission_classes = [IsAuthenticated]


class HostelProfileView(generics.RetrieveAPIView,generics.UpdateAPIView):
    serializer_class = HostelDetialsSerializer
    queryset = HostelProfile
    lookup_field = 'hostel_code'
    parser_classes = [IsAuthenticated, DjangoModelPermissions]


@api_view(['PUT'])
def change_room_price(request):
    if request.method == 'PUT':
        room_capacity = request.data['room_capacity']
        new_price = request.data['new_price']
        hostel = HostelProfile.objects.get(hostel_manager=request.user)
        try:
            update_room = RoomProfile.objects.filter(Hostel=hostel, Room_Capacity=room_capacity)
            update_room.update(Room_Price=new_price)
            return Response({'detail':'Room price have been updated'})

        except RoomProfile.DoesNotExist:
            return Response({'detail':'Room does not exist'})

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def edit_room_deatails(request):
    hostel_code = request.GET['hostelCode']
    room_no = request.GET['room_no']
    try:
        get_hostel = HostelProfile.objects.get(hostel_code=hostel_code)
        get_room = RoomProfile.objects.get(hostel=get_hostel, room_no=room_no)

    except RoomProfile.DoesNotExist:
          return Response({'messages':'Room Does not exist'}, status=status.HTTP_404_NOT_FOUND)

    except HostelProfile.DoesNotExist:
        return Response({'messages':'Hostel Does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        ser_room = RoomListSerializer(get_room, many=False)
        return Response(ser_room.data, status=status.HTTP_200_OK)    
    
    elif request.method == 'PUT':

        """Change the price of a specific room"""

        room_price = request.data['Room_Price']
        get_room.room_price = room_price
        get_room.save()
        ser_room = RoomListSerializer(get_room, many=False)
        return Response(ser_room.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_booking(request):

    """ Checking for a user booking """
    #for testing purposes

    booking_id = request.GET['booking_id']
    try:
        Booking.objects.filter(booking_id=booking_id).exists()
        get_booking = Booking.objects.get(booking_id=booking_id)
        info={'Student':get_booking.user.username,
                'Room Number':get_booking.room.room_no,
                'Hostel':get_booking.Hostel.hostel_name,
                'Verified':'Verified'}
        return Response(info)
    
    except Booking.DoesNotExist:
        info={'info':'Booking is not here'}
        return Response(info)
    
    
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def verify_tenant(request):
    tenant_id = request.POST['tenant_id']
    try:
        get_tenant = Tenant.objects.get(tenant_id=tenant_id)
        if request.method == 'GET':
        #if already checked in
            if get_tenant.checked_in == True:
                response={'Student':get_tenant.user.username,
                        'student-ID': get_tenant.user.student_id,
                        'Room Number':get_tenant.room.room_no,
                        'Hostel':get_tenant.hostel.hostel_name,
                        'Verified':'Already Checked In'}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response={'Student':get_tenant.user.username,
                        'Room Number':get_tenant.room.room_no,
                        'Hostel':get_tenant.hostel.hostel_name,
                        'Verified':'Verified'}
                get_tenant.checked_in = True
                get_tenant.save()
                return Response(response, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            get_tenant.delete()
            return Response({'message':'Tenant has been deleted'}) 
        
    except Tenant.DoesNotExist:
        info={'info':'Tenant is not verified'}
        return Response(info, status=status.HTTP_404_NOT_FOUND)
   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_tenants(request):
    hostelCode = request.GET['hostelCode']
    try:
        get_hostel = HostelProfile.objects.get(hostel_code=hostelCode)
        get_tenants = Tenant.objects.filter(hostel=get_booking).all()
        ser_tenants = TenantSerializer(get_tenants, many=True)
        return Response(ser_tenants.data)
    
    except HostelProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


