from .models import HostelProfile
from rest_framework import serializers


class HostelProfileSerializer(serializers.ModelSerializer):

    manager = serializers.SerializerMethodField(method_name='get_managers_name')
    class Meta:
        model = HostelProfile
        fields = ('hostel_name',
                  'manager',
                  'manager_contact',
                  'hostel_contact','other_phone',
                  'mobile_money',
                  'hostel_email',
                  'price_range',
                  'main_website',
                  'location',)
        
    def get_managers_name(self, obj):
        return obj.hostel_manager.username