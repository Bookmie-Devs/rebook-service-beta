"""Custom Imports"""
from typing import Any
from .models import Booking
from .models import Tenant
from accounts.models import Student
from rooms_app.models import RoomProfile

"""Built in Packages"""
from django.shortcuts import render
from django.views import generic
from django.http import (HttpRequest, 
                        HttpResponse, 
                        HttpResponseRedirect, 
                        JsonResponse)
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import timedelta
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required
from .decorators import login_required_htmx


@login_required_htmx
def book_room(request: HttpRequest) -> HttpResponse:     
    room_id = request.POST.get('room_id')
    student = Student.objects.get(user=request.user)
    room = RoomProfile.objects.get(room_id=room_id)

    if Tenant.objects.filter(student=student).exists():
        """
        Check if tenant exits
        """ 
        message ={'message':'Tenant is active'}
        return render(request,'htmx_message_templates/htmx_booking_message.html', message)
        # messages.info(request, 'Tenants can not book after payment',extra_tags=f'{room.room_id}')
        # # return redirect('accounts:booking-and-payments')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    elif request.user.gender.lower()!=room.gender.lower() and room.gender.lower()!='open':
        message ={'message':f'Room is for {room.gender}s'}
        return render(request,'htmx_message_templates/htmx_booking_message.html', message)
    
    elif Booking.objects.filter(student=student, payed=False).exists():
        """
        Check if room is full
        """
        messages.info(request, 'Booking active, proceed to payment or delete booking!!!', extra_tags="danger")
        # print(request.META.get(''))    
        # return redirect(request.META.get('HTTP_REFERER'))
        response = HttpResponse()
        response['HX-Redirect'] = resolve_url('accounts:booking-and-payments')
        return response
        # return redirect('accounts:booking-and-payments')
    
    elif not room.is_space_available():
        """
        Second check for room capacity
        """
        message ={'message':'Please room is full'}
        return render(request,'htmx_message_templates/htmx_booking_message.html', message)
        # messages.info(request, 'Please room is full')
        # # print(request.META.get(''))    
        # # return redirect(request.META.get('HTTP_REFERER'))
        # return redirect('accounts:booking-and-payments')

    # Check if room is occupied or avaialable for booking
    elif room.occupied or not room.is_available_for_booking():
        # message
        message ={'message':'Sorry room on pending for a user...'}
        return render(request,'htmx_message_templates/htmx_booking_message.html', message)
        # messages.info(request, 'Sorry, this room is on pending by other users for 1 hour, please select new one')
        # # print(request.META.get(''))    
        # # return redirect(request.META.get('HTTP_REFERER'))
        # return redirect('accounts:booking-and-payments')

    # Creating booking for user
    else:
        booked_room = RoomProfile.objects.get(room_id=request.POST.get('room_id')) 
        if not booked_room.is_free:
            #Saving booking info
            booking=Booking.objects.create(room=booked_room, student=student, hostel=booked_room.hostel, 
            student_id=student.student_id, status='Booked',)
            """
            Save booking model
            """
            booking.save()
            #redirect user for payment
            response = HttpResponse()
            response['HX-Redirect'] = resolve_url('accounts:booking-and-payments')
            return response
        response = HttpResponse()
        response['HX-Redirect'] = resolve_url('core:free-booking', room_id=booked_room.room_id)
        return response
        # return redirect('accounts:booking-and-payments')