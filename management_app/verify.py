from hostel_app.models import HostelProfile
from core.models import Tenant
from rest_framework.response import Response
from rest_framework import status

def verify(request=None, verification_code=None):
      # hostel of login manager 
    hostel = HostelProfile.objects.get(hostel_manager=request.user)
    try:
        tenant = Tenant.objects.get(
                            verification_code=verification_code,
                            hostel=hostel,
                            payed=True)
        # check if tenant is Vcode hasnt expired
        if tenant.is_active():
            #if already checked in
            if tenant.checked_in == True:
                response={'Verified':'Already Checked In',
                        'Student':tenant.user.username,
                        'student-ID': tenant.user.student_id,
                        'Room Number':tenant.room.room_no,
                        'Hostel':tenant.hostel.hostel_name,
                        }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response={'Student':tenant.user.username,
                        'Room Number':tenant.room.room_no,
                        'Hostel':tenant.hostel.hostel_name,
                        'Verified':'Verified'}
                # set check in if verified
                tenant.checked_in = True
                tenant.save()
                return Response(response, status=status.HTTP_200_OK)
        else:
            info={'message':'Tenant V-code has expired'}
            return Response(info, status=status.HTTP_404_NOT_FOUND)

    except Tenant.DoesNotExist:
        info={'message':'Tenant is not verified or has not payed'}
        return Response(info, status=status.HTTP_404_NOT_FOUND)