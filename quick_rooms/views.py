from django.http import HttpRequest
from django.shortcuts import redirect, render
from accounts.task import send_sms_task
from .models import AnonymousGuest
# Create your views here.


def quick_room_login(request: HttpRequest):
    if request.method=="POST":
        phone = request.POST.get('phone')
        if AnonymousGuest.objects.filter(phone=phone).exists():
            code = AnonymousGuest.objects.get(phone=phone)
            code.delete()
        new_otp = AnonymousGuest.objects.create(phone=phone)
        new_otp.save()  
        message=f"Your Private Code is {code.quest_code}. Don't ahre this code with anyone"
        send_sms_task(code.phone, message)
        return render(request, 'quick_rooms/htmx/confirm_privacy.html',)

    return render(request, 'quick_rooms/quick_privacy_login.html',)



def confirm_code(request: HttpRequest):
    phone = request.POST.get('code')
    if AnonymousGuest.objects.filter(phone=phone).exists():
        return redirect('quick-rooms:rooms')
    return render(request, 'quick_rooms/htmx/message.html', {'message':'Code not valid', 'tag':'danger'})
