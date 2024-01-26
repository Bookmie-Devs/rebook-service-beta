from django.conf import settings
from django.http import HttpRequest, Http404
from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from .serializers import (RoomListSerializer,
                          RoomDetailSerializer,
                          HostelDetialsSerializer,)

from rest_framework.authentication import SessionAuthentication
# from core.models import Booking
from .serializers import TenantListSerializer
from core.models import Tenant
from rest_framework import status
from .verify import verify
from hostel_app.models import HostelProfile
from django.utils import timezone
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated,
                                        DjangoModelPermissions) 
from .sales import convert_sales
from rest_framework.decorators import (permission_classes,
                                       authentication_classes)
from rooms_app.models import RoomProfile
from django.db.models import Q
from rest_framework import generics

# custom permissions
from .custom_permissions import IsHostelManager


class RoomListView(generics.ListAPIView):
    queryset = HostelProfile.objects.all()
    serializer_class = RoomListSerializer

    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,
                          IsHostelManager, 
                          DjangoModelPermissions]

    def get(self, request, *args, **kwargs):

        """Gets a list of all rooms related to 
    a particular hostel after getting the hostel code from the person who logs in"""
        
        try:
            get_hostel=HostelProfile.objects.get(hostel_manager=request.user)
            get_rooms = RoomProfile.objects.filter(hostel=get_hostel)
            serializer = RoomListSerializer(get_rooms, many=True)
            return Response(serializer.data)
        
        except HostelProfile.DoesNotExist:

            return Response({'message':'Hostel Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

class RoomDetailView(generics.RetrieveUpdateAPIView):

    # SessionAuthentication for testing
    # authentication_classes = [SessionAuthentication]
    
    permission_classes = [IsAuthenticated,
                          IsHostelManager, 
                          DjangoModelPermissions,]

    serializer_class = RoomDetailSerializer
    queryset = RoomProfile.objects.all()
    lookup_field = "room_id"



class HostelProfileView(generics.RetrieveUpdateAPIView):

        # SessionAuthentication for testing
    # authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated,
                          IsHostelManager, 
                          DjangoModelPermissions]

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


# update room prices
class UpdateRoomPrice(generics.UpdateAPIView):
        
    permission_classes = [IsAuthenticated,
                          IsHostelManager, 
                          DjangoModelPermissions]

    queryset =RoomProfile.objects.all()

    def update(self, request, *args, **kwargs):
        room_capacity = request.data.get('room_capacity') #room with capacity
        new_price = request.data.get('new_price') #price for those rooms
        hostel = HostelProfile.objects.get(hostel_manager=request.user)
        # check if room exist
        if RoomProfile.objects.filter(hostel=hostel, room_capacity=room_capacity).exists():
            update_room = RoomProfile.objects.filter(hostel=hostel, room_capacity=room_capacity)
            # calculate ptf_pricing 
            addtional_pricing: float = float(new_price) * settings.SUPPLY_COST_PERCENTAGE
            new_ptf_room_price = float(new_price) + float(addtional_pricing)

            update_room.update(room_price=new_price, ptf_room_price=new_ptf_room_price)
            return Response({'message':'Rooms price have been updated'}, status=status.HTTP_201_CREATED)
        
        else: 
            return Response({'message':'Rooms does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    
# List Tenant View
class TenantListView(generics.ListAPIView):
        
    # SessionAuthentication for testing
    # authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated, 
                          DjangoModelPermissions]
    
    queryset = Tenant.objects.all()
    serializer_class = TenantListSerializer

    def get(self, request, *args, **kwargs):
        try:
            get_hostel = HostelProfile.objects.get(hostel_manager=request.user)
            get_tenants = Tenant.objects.filter(hostel=get_hostel).all()

            if get_tenants is not None:
                serializer = TenantListSerializer(get_tenants, many=True)
                return Response(serializer.data)
            
            else:
                return Response({"message":"No Tenants Yet"},status=status.HTTP_404_NOT_FOUND)

    
        except HostelProfile.DoesNotExist:
            return Response({'message':'Hostel was not found'} ,status=status.HTTP_404_NOT_FOUND)
        

class SalesStatsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsHostelManager]  

    # authentication_classes = [SessionAuthentication]
    def get(self, request: HttpRequest):
        from .models import SalesStatistics
        try:
            hostel = HostelProfile.objects.get(hostel_manager=request.user)
            sales = SalesStatistics.objects.filter(hostel=hostel).all()
            return Response(convert_sales(sales=sales), status=status.HTTP_200_OK)
        except:
            return Response({'MESSAGE':'NO_DATA_FOUND'},status=status.HTTP_404_NOT_FOUND)
        

@permission_classes([IsAuthenticated])    
@api_view(['POST'])
def verify_tenant(request):
    verification_code = request.data.get('verification_code')
    
    # Verify Tenant
    return verify(request=request, verification_code=verification_code)
  