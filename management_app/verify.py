from django.http import HttpRequest
from hostel_app.models import HostelProfile
from core.models import Tenant
from rest_framework.response import Response
from rest_framework import status
from .serializers import TenantVerificationSerializer

def verify(request: HttpRequest=None, verification_code: str=None):
    try:
        tenant = Tenant.objects.get(verification_code=verification_code, payed=True)
        
        # check if tenant is Vcode hasnt expired
        if tenant.is_active():
            
            serializer = TenantVerificationSerializer(tenant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            info={'message':'Tenant V-code has expired'}
            return Response(info, status=status.HTTP_404_NOT_FOUND)

    except Tenant.DoesNotExist:
        info={'message':'Tenant is not verified or has not payed'}
        return Response(info, status=status.HTTP_404_NOT_FOUND)