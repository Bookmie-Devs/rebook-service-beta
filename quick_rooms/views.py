from django.http import HttpRequest, HttpResponse
from campus_app.models import CampusProfile
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.urls import resolve
from django.conf import settings
from accounts.task import send_sms_task
from payments_app.payStack import payment_is_confirm, paystack_verification
from .models import AnonymousGuest, GuestHouseRoom, GuestBooking, GuestPaymentHistory, PaystackGuestHouseSubAccount
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
# Create your views here.


def request_code(request: HttpRequest, room_id):
    if request.method=="POST":
        phone = request.POST.get('phone')
        if AnonymousGuest.objects.filter(phone=phone).exists():
            code = AnonymousGuest.objects.get(phone=phone)
            code.delete()
        new_otp = AnonymousGuest.objects.create(phone=phone)
        new_otp.save()  
        message = f"Your Bookmie Privacy Code is {new_otp.quest_code}"
        send_sms_task(phone, message)
        return render(request, 'quick_rooms/htmx/confirm_privacy.html',{'room_id':room_id})

    return render(request, 'quick_rooms/quick_privacy_login.html',{'room_id':room_id})


@require_http_methods(['POST'])
def generate_private_booking(request: HttpRequest):
    quest_code = request.POST.get('code')
    room_id = request.POST.get('room_id')
    if AnonymousGuest.objects.filter(quest_code=quest_code).exists():
        private_user = AnonymousGuest.objects.get(quest_code=quest_code)
        room = GuestHouseRoom.objects.get(room_id=room_id)
        booking = GuestBooking.objects.create(guest_user=private_user, campus=room.campus, room=room, guest_house=room.guest_house)
        booking.save()
        response = HttpResponse()
        response['HX-Redirect']=resolve_url('quick-rooms:profile', booking_id=booking.booking_id)
        return response
    else:
        return render(request, 'quick_rooms/htmx/message.html', {'message':'Code not valid', 'tag':'danger'})


def rooms(request: HttpRequest, campus_id):
    campus = CampusProfile.objects.get(campus_id=campus_id)
    rooms = GuestHouseRoom.objects.filter(campus=campus).all()
    return render(request, 'quick_rooms/quick_rooms.html', {'rooms':rooms, 'campus':campus})


def book_room(request: HttpRequest):
    room_id = request.POST.get('room_id')
    response = HttpResponse()
    response['HX-Redirect']=resolve_url('quick-rooms:secure-privacy-code', room_id=room_id)
    return response


def private_payment(request, booking_id):
    booking = GuestBooking.objects.get(booking_id=booking_id)
    payment = GuestPaymentHistory.objects.create(amount=booking.room.ptf_room_price,booking=booking,)
    payment.save()
    subaccount = PaystackGuestHouseSubAccount.objects.get(guest_house=payment.booking.guest_house)
    return render(request, 'quick_rooms/make_payment.html', {'payment':payment, 'subaccount':subaccount,
                                                             'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})


def verify_quick_room_payment(request,  reference_id, paystack_reference, booking_id):
    payment = get_object_or_404(GuestPaymentHistory, reference_id=reference_id)
    booking = GuestBooking.objects.get(booking_id=booking_id)
    response_data = paystack_verification(paystack_reference)
    if payment_is_confirm(data=response_data, amount=payment.amount):
        booking.payed = True
        booking.save()
        payment.successful =True
        payment.save()
    else:
        pass
    
    pass


def profile(request: HttpRequest, booking_id):
    context = {'is_private_booking':True}

    if GuestBooking.objects.filter(booking_id=booking_id).exists():
        booking = GuestBooking.objects.get(booking_id=booking_id)
        tenant = False
        context.update({'booking': booking,})
        return render(request, 'booking_and_payments.html',context=context)
    
    # elif Tenant.objects.filter(student=student).exists():
    #     tenant = Tenant.objects.get(student=student)
    #     booking = False
    #     context.update({'tenant':tenant,'booking': booking,})
    #     return render(request, 'booking_and_payments.html',context=context)
    
    else:
        return render(request, 'booking_and_payments.html', context=context)


class PrivacyPolicyView(TemplateView):

    template_name = 'quick_rooms/privacy_policy.html'
