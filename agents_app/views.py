from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render
from rest_framework.response import Response
from agents_app.models import Agent
from campus_app.models import CampusProfile
from hostel_app.models import HostelProfile
from rooms_app.models import RoomProfile
from .serializers import AgentHostelProfileSerializer,  AgentHostelListSerializer, HostelCreationSerializer, RoomListSerializer, RoomProfileSerializer
from rest_framework import status
from hostel_app.models import Banks
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from management_app.custom_permissions import IsBookmieAgent
from django.db.models import F
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBookmieAgent])
# @authentication_classes([SessionAuthentication])
def agent_hostels(request: HttpRequest):
    try:
        agent = Agent.objects.get(user=request.user, is_verified=True, is_active=True)
        agent_hostels = HostelProfile.objects.filter(agent_affiliate=agent).all()
        serializer = AgentHostelListSerializer(agent_hostels, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Agent.DoesNotExist:
        return Response(data={'message':'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET', 'POST',])
@permission_classes([IsAuthenticated, IsBookmieAgent])
# @authentication_classes([SessionAuthentication])
def agent_hostel_profile(request: HttpRequest, hostel_code):
    from .registrations import register_room
    try:
        agent = Agent.objects.get(user=request.user, is_verified=True, is_active=True)
        agent_hostel = HostelProfile.objects.get(agent_affiliate=agent, hostel_code=hostel_code)
        if request.method=='POST':
            register = register_room(hostel=agent_hostel, room_no=request.data.get('room_number'), 
                          room_price=request.data.get('room_price'),agent=agent, gender=request.data.get('gender'),
                          bed_space_left=request.data.get('bed_space_left'), floor_number=request.data.get('floor_number'),
                          )
            if register==201:
                return Response(data={'message':'Room created'}, status=status.HTTP_201_CREATED)
            else:
                return Response(data={'message':'Room not created'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AgentHostelProfileSerializer(agent_hostel)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Agent.DoesNotExist:
        return Response(data={'message':'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBookmieAgent])
# @authentication_classes([SessionAuthentication])
def agent_registered_rooms(request: HttpRequest):
    try:
        agent = Agent.objects.get(user=request.user, is_verified=True, is_active=True)
        agent_rooms = RoomProfile.objects.filter(hostel__agent_affiliate=agent)
        serializer = RoomListSerializer(agent_rooms, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Agent.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN)


class RoomProfileView(generics.RetrieveUpdateAPIView):
    lookup_field = 'room_id'
    serializer_class = RoomProfileSerializer
    queryset = RoomProfile.objects.all()



class HostelCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsBookmieAgent]
    serializer_class = HostelCreationSerializer
    queryset = HostelProfile.objects.all()

@api_view(['GET'])
def get_campuses(request: HttpRequest):
    campuses = {}
    for campus in CampusProfile.objects.filter(available_on_campus=True).all():
        campuses.update({int(campus.pk): campus.alias_name.title()}) 
    return Response(campuses, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBookmieAgent])
def get_bank_codes(request: HttpRequest):
    banks = {}
    for bank_code, bank_name in Banks:
        banks.update({bank_code: bank_name}) 
    return Response(banks, status=status.HTTP_200_OK)