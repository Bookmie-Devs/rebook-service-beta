from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render
from rest_framework.response import Response
from agents_app.models import HostelAgent
from hostel_app.models import HostelProfile
from rooms_app.models import RoomProfile
from .serializers import AgentHostelSerializer,  AgentHostelListSerializer
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.db.models import F
# Create your views here.

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
def agent_hostels(request: HttpRequest):
    try:
        agent = HostelAgent.objects.get(user=request.user, is_verified=True, is_active=True)
        agent_hostels = HostelProfile.objects.filter(agent_affiliate=agent, verified=True).all()
        serializer = AgentHostelListSerializer(agent_hostels, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except HostelAgent.DoesNotExist:
        return Response(data={'message':'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET', 'POST',])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
def agent_hostel_profile(request: HttpRequest, hostel_id):
    from .registrations import register_room
    try:
        agent = HostelAgent.objects.get(user=request.user, is_verified=True, is_active=True)
        agent_hostel = HostelProfile.objects.get(agent_affiliate=agent, hostel_id=hostel_id, verified=True)
        if request.method=='POST':
            register = register_room(hostel=agent_hostel, room_no=request.data.get('room_number'), 
                          room_price=request.data.get('room_price'),agent=agent, gender=request.data.get('gender'),
                          bed_space_left=request.data.get('bed_space_left'), floor_number=request.data.get('floor_number'),
                          )
            if register==201:
                return Response(data={'message':'Room created'}, status=status.HTTP_201_CREATED)
            else:
                return Response(data={'message':'Room not created'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AgentHostelSerializer(agent_hostel)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except HostelAgent.DoesNotExist:
        return Response(data={'message':'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
    


def agent_rooms(request: HttpRequest):
    agent = HostelAgent.objects.get(user=request.user, is_verified=True, is_active=True)
    agent_hostel = RoomProfile.objects.get(F('hostel'), verified=True)


def agent_room_profile(request):
    pass