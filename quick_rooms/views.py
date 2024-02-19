from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, resolve_url
from django.urls import resolve
from accounts.task import send_sms_task
from .models import AnonymousGuest, GuestHouseRoom
from django.views.decorators.http import require_http_methods
# Create your views here.


def quick_room_login(request: HttpRequest):
    if request.method=="POST":
        phone = request.POST.get('phone')
        if AnonymousGuest.objects.filter(phone=phone).exists():
            code = AnonymousGuest.objects.get(phone=phone)
            code.delete()
        new_otp = AnonymousGuest.objects.create(phone=phone)
        new_otp.save()  
        message = f"Your Bookmie Privacy Code is {new_otp.quest_code}"
        send_sms_task(code.phone, message)
        return render(request, 'quick_rooms/htmx/confirm_privacy.html',)

    return render(request, 'quick_rooms/quick_privacy_login.html',)


@require_http_methods(['POST'])
def confirm_code(request: HttpRequest):
    phone = request.POST.get('code')
    if AnonymousGuest.objects.filter(phone=phone).exists():
        code = AnonymousGuest.objects.get(phone=phone)
        code.delete()
        response = HttpResponse()
        response['HX-Redirect']=resolve_url('quick-rooms:rooms')
        return response
    return render(request, 'quick_rooms/htmx/message.html', {'message':'Code not valid', 'tag':'danger'})


def rooms(request: HttpRequest):
    rooms = GuestHouseRoom.objects.all()
    return render(request, 'quick_rooms/quick_rooms.html', {'rooms':rooms})