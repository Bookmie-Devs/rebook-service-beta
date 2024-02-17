from rest_framework.serializers import ModelSerializer
from .models import HostelAgent

class AgenProfilesSerilizer(ModelSerializer):
    class Meta:
        model = 