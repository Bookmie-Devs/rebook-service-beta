from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializers import HostellistSerializer
from hostel_app.models import HostelProfile
from campus_app.models import CampusProfile
from campus_app.serializers import CampusSerializer
from rest_framework import status


class HostelListView(ListAPIView):
    serializer_class = HostellistSerializer
    queryset = HostelProfile.objects.all()

    def get(self, request,campus_code, *args, **kwargs):
        
        campus = CampusProfile.objects.get(campus_code=campus_code)
        """Gets a list of all hostels related to 
        a particular campus after getting the campus code from the person who logs in"""
        
        # try:  
        hostels=HostelProfile.objects.filter(campus=campus).all()
        hostel_serializer = HostellistSerializer(hostels, many=True)

        # campus serializer
        campus_serializer = CampusSerializer(campus, many=False)

        data = {
            'campus': campus_serializer.data,
            'hostels': hostel_serializer.data,
            }  
        
        return Response(data=data)
    
        # except:
        #     return Response({'message':'No hostels found'}, status=status.HTTP_404_NOT_FOUND)
        