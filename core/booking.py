"""Custom Imports"""
from typing import Any
from .models import Booking
from .models import Tenant
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
    room = RoomProfile.objects.get(room_id=room_id)

    if Tenant.objects.filter(user=request.user).exists():
        """
        Check if tenant exits
        """ 
        message ={'message':'Tenant is active'}
        return render(request,'htmx_message_templates/htmx_booking_message.html', message)
        # messages.info(request, 'Tenants can not book after payment',extra_tags=f'{room.room_id}')
        # # return redirect('accounts:booking-and-payments')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    elif request.user.gender.lower()!=room.gender.lower():
        message ={'message':f'Room is for {room.gender}s'}
        return render(request,'htmx_message_templates/htmx_booking_message.html', message)
    
    elif Booking.objects.filter(user=request.user, payed=False).exists():
        """
        Check if room is full
        """
        messages.info(request, 'You already booked for a room please proceed to payment or delete booking!!!')
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
        student_id = request.user.student_id  
        booked_room = RoomProfile.objects.get(room_id=request.POST.get('room_id')) 
        #Saving booking info
        booking=Booking.objects.create(room=booked_room, user=request.user, 
        room_number=booked_room.room_no, hostel=booked_room.hostel, 
        student_id=student_id, status='Booked',campus=booked_room.campus)
        """
        Save booking model
        """
        booking.save()
        
        #redirect user for payment
        response = HttpResponse()
        response['HX-Redirect'] = resolve_url('accounts:booking-and-payments')
        return response
        # return redirect('accounts:booking-and-payments')