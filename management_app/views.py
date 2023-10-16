from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from .serializers import (RoomListSerializer,
                          RoomDetailSerializer,
                          HostelDetialsSerializer)

from rest_framework.authentication import SessionAuthentication
# from core.models import Booking
from .serializers import TenantSerializer
from core.models import Tenant
from rest_framework import status
from hostel_app.models import HostelProfile
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        DjangoModelPermissions) 

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

    # SessionAuthentication for testing
    authentication_classes = [SessionAuthentication]

    permission_classes = [DjangoModelPermissions]

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

    # SessionAuthentication for testing
    authentication_classes = [SessionAuthentication]
    
    permission_classes = [DjangoModelPermissions]

    serializer_class = RoomDetailSerializer
    queryset = RoomProfile.objects.all()
    lookup_field = "room_id"



class HostelProfileView(generics.RetrieveUpdateAPIView):

        # SessionAuthentication for testing
    authentication_classes = [SessionAuthentication]

    permission_classes = [IsHostelManager, DjangoModelPermissions]

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
        
    # SessionAuthentication for testing
    authentication_classes = [SessionAuthentication]

    permission_classes = [DjangoModelPermissions]

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
        
    
@api_view(['POST'])

# SessionAuthentication for testing
@authentication_classes([SessionAuthentication])
def verify_tenant(request):
    verification_code = request.data.get('verification_code')

    # hostel of login manager 
    hostel = HostelProfile.objects.get(hostel_manager=request.user)

    try:
        get_tenant = Tenant.objects.get(
                            verification_code=verification_code,
                            hostel=hostel,
                            payed=True)
        
        #if already checked in
        if get_tenant.checked_in == True:

            response={'Verified':'Already Checked In',
                     'Student':get_tenant.user.username,
                     'student-ID': get_tenant.user.student_id,
                     'Room Number':get_tenant.room.room_no,
                     'Hostel':get_tenant.hostel.hostel_name,
                    }
            return Response(response, status=status.HTTP_200_OK)

        else:
            response={'Student':get_tenant.user.username,
                    'Room Number':get_tenant.room.room_no,
                    'Hostel':get_tenant.hostel.hostel_name,
                    'Verified':'Verified'}
            
            # set check in if verified
            get_tenant.checked_in = True
            get_tenant.save()
            return Response(response, status=status.HTTP_200_OK)

    except Tenant.DoesNotExist:
        info={'message':'Tenant is not verified or has not payed'}
        return Response(info, status=status.HTTP_404_NOT_FOUND)
   

# List Tenant View
class TenantListView(generics.ListAPIView):
        
    # SessionAuthentication for testing
    authentication_classes = [SessionAuthentication]

    permission_classes = [DjangoModelPermissions]
    
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def get(self, request, *args, **kwargs):
        try:
            get_hostel = HostelProfile.objects.get(hostel_manager=request.user)
            get_tenants = Tenant.objects.filter(hostel=get_hostel).all()

            if get_tenants is not None:
                serializer = TenantSerializer(get_tenants, many=True)
                return Response(serializer.data)
            
            else:
                return Response({"message":"No Tenants Yet"},status=status.HTTP_404_NOT_FOUND)

    
        except HostelProfile.DoesNotExist:
            return Response({'message':'Hostel was not found'} ,status=status.HTTP_404_NOT_FOUND)