from rest_framework.generics import (RetrieveAPIView,
                                     ListAPIView)
from rest_framework.response import Response
from rest_framework import status
from .models import HostelProfile
from .serializers import HostelProfileSerializer, HostelRoomsSerializer

class HostelProfileView(RetrieveAPIView):

    lookup_field ="hostel_id"

    queryset = HostelProfile.objects.all()
    serializer_class = HostelProfileSerializer



class HostelRoomsView(ListAPIView):

    def get(self, request, hostel_id, *args, **kwargs):
        hostel_rooms = HostelProfile.objects.filter(hostel_id=hostel_id).all()
        serializer = HostelRoomsSerializer(hostel_rooms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
