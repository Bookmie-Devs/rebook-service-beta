from rest_framework import generics
from rest_framework.response import Response
from .models import HostelProfile
from .serializers import HostelProfileSerializer

class HostelProfileView(generics.RetrieveAPIView):

    lookup_field ="hostel_id"

    queryset = HostelProfile.objects.all()
    serializer_class = HostelProfileSerializer


