from rest_framework.serializers import ModelSerializer
from .models import CampusProfile


class CampusSerializer(ModelSerializer):
    class Meta:
        model = CampusProfile
        fields = ('campus_name','campus_code',)


