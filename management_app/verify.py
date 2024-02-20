from django.http import HttpRequest
from hostel_app.models import HostelProfile
from core.models import Tenant
from .models import Management
from rest_framework.response import Response
from rest_framework import status
from .serializers import TenantVerificationSerializer

def verify(request: HttpRequest=None, verification_code: str=None):
    try:
        # worker who is login to verify tenant
        if Management.objects.filter(user=request.user, is_active=True).exists():
            portar = Management.objects.get(user=request.user, is_active=True)
            tenant = Tenant.objects.get(verification_code=verification_code, payed=True)
            # check if tenant is Vcode hasnt expired
            if tenant.is_active():
                if tenant.hostel!=portar.hostel:
                    info={"message":f"Code is assign to {tenant.hostel.hostel_name}"}
                    return Response(info, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Return This if everything is valid
                    serializer = TenantVerificationSerializer(tenant)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                info={'message':'Tenant V-code has expired'}
                return Response(info, status=status.HTTP_401_UNAUTHORIZED)
        else:
            info={'message':'Portar in no Verified'}
            return Response(info, status=status.HTTP_403_FORBIDDEN)
            
    except Tenant.DoesNotExist:
        info={'message':'Tenant V-code not valid.'}
        return Response(info, status=status.HTTP_404_NOT_FOUND)