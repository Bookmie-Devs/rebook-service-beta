"""Custom imports"""
from django.http import HttpRequest

from config import settings
from payments_app.payStack import payment_is_confirm, paystack_verification
from .models import PaymentHistory, PaystackSubAccount
from accounts.models import Student
from rooms_app.models import RoomProfile
from core.models import Booking, Tenant

"""Packeges """
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect


@login_required()
def initiate_part_payment(request: HttpRequest, room_id):
    student = Student.objects.get(user=request.user)
    booking = Booking.objects.get(student=student)
    room = RoomProfile.objects.get(room_id=room_id)
    if booking._has_expired():
        booking.delete()
        messages.info(request, 'Sorry, Booking has expired please book another room', extra_tags="danger")
        return redirect('accounts:booking-and-payments')

    if request.method=='POST':
        """
        Check if booking is for upadting vcode
        and create a new payment history and skip the
        check for if room is occupied (beacuse at the time of update it will surely be occcupied)
        """
        if booking.is_updating_vcode:
            #save payment details
            payment = PaymentHistory.objects.create(
            student=student,
            email=request.POST.get('email'),
            amount=room.half_pricing,
            account_payed_to=room.hostel.account_number,
            room=room,
            hostel=room.hostel, is_half_payment=True
            )
            payment.save()            
            return redirect('payments:make-payment', reference_id=payment.reference_id, room_id=room.room_id)

        elif room.occupied:
            messages.info(request, 'Sorry, room has just been occupied by someone, please select new one')
            booking.delete()
            return redirect('accounts:booking-and-payments')

        else:
            if PaymentHistory.objects.filter(student=student, successful=False).exists():
                # check if there is an unsuccessful payment
                PaymentHistory.objects.filter(student=student, successful=False).delete()
                    #save payment details
                payment = PaymentHistory.objects.create(
                student=student,
                amount=room.half_pricing,
                room=room,
                hostel=room.hostel,  
                is_half_payment=True,
                email=request.POST.get('email'),
                account_payed_to=room.hostel.account_number,
                )
                payment.save()
                return redirect('payments:make-payment', reference_id=payment.reference_id, room_id=room.room_id)
            else:
                #save payment details
                payment = PaymentHistory.objects.create(student=student,
                email=request.POST.get('email'),
                amount=room.half_pricing,
                account_payed_to=room.hostel.account_number,
                room=room,
                hostel=room.hostel,  
                is_half_payment=True
                )
                payment.save()            
                return redirect('payments:make-payment', reference_id=payment.reference_id, room_id=room.room_id)
    is_part_payment = True       
    # return redirect
    return render(request, 'payments/initiate_payment.html', {'room':room, 'is_part_payment':is_part_payment, 'student':student,})


def complete_part_payment(request: HttpRequest):
    student = Student.objects.get(user=request.user)
    try:
        tenant=Tenant.objects.get(student=student, made_part_payment=True)
        # payment = get_object_or_404(PaymentHistory, user=request.user, reference_id=reference_id)
         #save payment details
        payment = PaymentHistory.objects.create(
        student=student,
        email=request.user.email,
        amount=tenant.amount_left_to_pay,
        account_payed_to=tenant.room.hostel.account_number,
        room=tenant.room,
        hostel=tenant.room.hostel, completed_full_payment=True
        )
        payment.save()    
        subaccount = PaystackSubAccount.objects.get(hostel=tenant.room.hostel)
        # make payment ot subaccount
        context={
        'amount':payment.amount,
        'reference_id': payment.reference_id, 
        'amount_value':payment.get_amount_value(),
        'subaccount':subaccount.subaccount_code,
        'student':student, 'is_completing_payment':True,
        'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY 
        }
        return render(request,'payments/make_payment.html', context)
    
    except Tenant.DoesNotExist:
        messages.info(request, 'You dont have any outstanding debt', extra_tags='danger')
        return redirect('accounts:booking-and-payments')
    
@login_required()
def verify_complete_payment(request: HttpRequest, reference_id, paystack_reference):  
    student = Student.objects.get(user=request.user)
    payment = get_object_or_404(PaymentHistory, student=student, reference_id=reference_id)
    tenant=Tenant.objects.get(student=student, made_part_payment=True)
    # room payed for    
    acquired_room = RoomProfile.objects.get(room_id=payment.room.room_id)

    # checkout validation from api response after passing paystack_reference
    response_data = paystack_verification(paystack_reference)
    # confrim payment
    if payment_is_confirm(data=response_data, amount=payment.amount):
        tenant.completed_payment=True
        tenant.made_part_payment=False
        tenant.amount_left_to_pay=0.0
        tenant.save()
        payment.completed_full_payment =True
        payment.successful =True
        payment.save()
        messages.info(request, 'Completed Payment', extra_tags='success')
        return redirect('accounts:booking-and-payments')