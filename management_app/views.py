from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from .serializers import (RoomListSerializer,
                          RoomDetailSerializer,
                          HostelDetialsSerializer)

from rest_framework.authentication import SessionAuthentication
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


class RoomListView(generics.ListAPIView):
    queryset = HostelProfile.objects.all()
    serializer_class = RoomListSerializer

    # SessionAuthentication for testing
    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get(self, request, *args, **kwargs):

        """Gets a list of all rooms related to 
    a particular hostel after getting the hostel code from the person who logs in"""
        
        try:
            hostel_code = request.data.get('hostel_code')
            get_hostel=HostelProfile.objects.get(hostel_manager=request.user)
            get_rooms = RoomProfile.objects.filter(hostel=get_hostel)
            serializer = RoomListSerializer(get_rooms, many=True)
            return Response(serializer.data)
        
        except HostelProfile.DoesNotExist:

            return Response({'detail':'Hostel Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

class RoomDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = RoomDetailSerializer
    queryset = RoomProfile.objects.all()
    lookup_field = "room_id"

     # SessionAuthentication for testing
    authentication_classes = [SessionAuthentication]
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class HostelProfileView(generics.RetrieveAPIView,generics.UpdateAPIView):
    serializer_class = HostelDetialsSerializer
    queryset = HostelProfile.objects.all()

    def get(self, request, *args, **kwargs):
        hostel = HostelProfile.objects.get(hostel_manager=request.user)
        #serialized data
        serializer = HostelDetialsSerializer(hostel)   

        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        hostel = HostelProfile.objects.get(hostel_manager=request.user)

        serializer = HostelDetialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.update(instance=hostel, validated_data=request.data)

        return Response(serializer.data)
    
    # SessionAuthentication for testing
    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated, DjangoModelPermissions]


# update room prices
class UpdateRoomPrice(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset =RoomProfile.objects.all()


    def update(self, request, *args, **kwargs):
        room_capacity = request.data['room_capacity'] #room with capacity
        new_price = request.data['new_price'] #price for those rooms
        hostel = HostelProfile.objects.get(hostel_manager=request.user)
        try:
            update_room = RoomProfile.objects.filter(hostel=hostel, room_capacity=room_capacity)
            update_room.update(room_price=new_price)
            return Response({'detail':'Rooms price have been updated'}, status=status.HTTP_201_CREATED)

        except RoomProfile.DoesNotExist:
            return Response({'detail':'Rooms does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

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
    verification_code = request.POST['verification_code']
    try:
        get_tenant = Tenant.objects.get(verification_code=verification_code)
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
    try:
        get_hostel = HostelProfile.objects.get(hostel_code=request.user)
        get_tenants = Tenant.objects.filter(hostel=get_booking).all()
        ser_tenants = TenantSerializer(get_tenants, many=True)
        return Response(ser_tenants.data)
    
    except HostelProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


