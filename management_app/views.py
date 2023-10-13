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


class HostelProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = HostelDetialsSerializer
    queryset = HostelProfile.objects.all()

    def get(self, request, *args, **kwargs):
        hostel = HostelProfile.objects.get(hostel_manager=request.user)
        #serialized data
        serializer = HostelDetialsSerializer(hostel)   

        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        hostel = HostelProfile.objects.get(hostel_manager=request.user)

        serializer = HostelDetialsSerializer(instance=hostel, data=request.data)
        serializer.is_valid(raise_exception=True)

        # save and update
        self.perform_update(serializer)

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
        
    
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def verify_tenant(request):
    verification_code = request.data.get('verification_code')
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
        get_tenants = Tenant.objects.filter(hostel=get_hostel).all()

        if get_tenants is not None:
            serializer = TenantSerializer(get_tenants, many=True)
            return Response(serializer.data)
        
        else:
            return Response({"message":"No Tenants Yet"},status=status.HTTP_404_NOT_FOUND)

    
    except HostelProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


