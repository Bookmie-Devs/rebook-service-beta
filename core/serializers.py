from rest_framework import serializers
from hostel_app.models import HostelProfile
from django.urls import reverse

class HostellistSerializer(serializers.ModelSerializer):
    
    # gets and return the method "get_absolute_view_url" into the fileds
    absolute_url = serializers.SerializerMethodField(
                        method_name= 'get_absolute_url',
                        read_only=True)
    class Meta:
        model=HostelProfile
        fields =('hostel_name',
                 'hostel_image',
                 'category',
                 'location',
                 'price_range',
                 'absolute_url',
                 )

    # Return the deatail url for the each room in the list
    def get_absolute_url(self, obj):
        return reverse('hostels:api-hostel-profile',
                        kwargs={'hostel_id':obj.hostel_id},
                        )
