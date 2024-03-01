from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from accounts.models import OtpCodeData
from rest_framework.permissions import IsAuthenticated
from accounts.task import send_sms_task
from rest_framework.response import Response
from rest_framework import status
from management_app.custom_permissions import IsHostelAgent

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsHostelAgent])  
def get_otp_phone(request: HttpRequest):
    if OtpCodeData.objects.filter(user=request.user).exists():
        code = OtpCodeData.objects.get(user=request.user)
        code.delete()
    new_otp = OtpCodeData.objects.create(user=request.user)
    new_otp.save()  
    message = f"Your Bookmie Agent Code is {new_otp.otp_code}"
    # send_sms_task.delay(request.user.phone, msg)
    # for testing
    send_sms_task(request.user.phone, message)
    return Response({'message':'Office Code Sent'}, status=status.HTTP_200_OK)
