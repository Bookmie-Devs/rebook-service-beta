from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from campus_app.models import CampusProfile
from core.serializers import BookingSerializer, TenantSerializer
from .serializers import UserSerializer
from .models import CustomUser
from django.conf import settings
from core.models import Booking, Tenant


@api_view(['POST'])
def signup_api_view(request):
    if request.method == 'POST':
        if CampusProfile.objects.filter(campus_code=str(request.data.get('campus')).upper().strip()).exists():
            ##Getting campus model for quering hostels related to it
            get_campus=CampusProfile.objects.get(campus_code=str(request.data.get('campus')).upper().strip())

            ##checks if password if equal
            if request.data.get('password') == request.data.get('confirm_password'):
                    
                    #existance of phone number 
                    if CustomUser.objects.filter(phone=request.data.get('phone')).exists():
                        return Response({'message':'Phone Number already registered'})
                    
                    elif CustomUser.objects.filter(email=request.data.get('email')).exists():
                        return Response({'message':'Eamil has already been registered'})
                    
                    elif CustomUser.objects.filter(student_id = request.data.get('student_id')).exists():
                        return Response({'message':'Stundent has already been registered'})

                    else:
                        """Creation of user model with details submitted"""
                        create_user: CustomUser = CustomUser.objects.create_user(first_name=request.data.get('first_name'), 
                            last_name=request.data.get('last_name'), middle_name=request.data.get('middle_name') ,
                            email=request.data.get('email'), campus=get_campus, 
                            username=f"{request.data.get('first_name')}_{request.data.get('middle_name')} {request.data.get('last_name')}",

                            password=request.data.get('password'), phone=request.data.get('phone'), 
                            student_id=request.data.get('student_id'),)
                        create_user.save()

                        send_mail(from_email=settings.EMAIL_HOST_USER, 
                        recipient_list=[request.user.email], 
                        subject=f'Congrats {request.user.username}. Your Sign Up seccessfull', 
                        message=render_to_string('emails/signup_congrat.html',{'user':request.user}),
                        fail_silently=True)
                          
                        """return token to user after user have been registed"""
                        return TokenObtainPairView.as_view({'email':create_user.emai,'password':request.data.get('password')})
                    
            else:
                return Response(data={'message':'Password is not matching'},status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(data={'message':'BookUp is not yet registered on your campus'},status=status.HTTP_400_BAD_REQUEST)
        
    # return render(request, 'forms/signup.html',)  

@permission_classes([IsAuthenticated])
def booking_and_payments(request):
    get_user = CustomUser.objects.get(id=request.user.id)

    if Booking.objects.filter(user=request.user).exists():
        booking = Booking.objects.get(user=request.user)
        tenant = False
        context = {'user':UserSerializer(get_user, many=False).data, 
                   'tenant':tenant,
                   'booking': BookingSerializer(booking, many=False).data,
                   }
        return Response(data=context)

    elif Tenant.objects.filter(user=request.user).exists():
        tenant = Tenant.objects.get(user=request.user)
        booking = False
        context = {'user':UserSerializer(get_user, many=False).dat, 
                   'booking': booking,
                   'tenant':TenantSerializer(instance=tenant,many=False).data}
        return Response(data=context)
    
    else:
        return Response(data={'user':UserSerializer(instance=get_user, many=False),
                              'booking':False,
                              'tenant':False,})