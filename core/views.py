
"""Custom Imports"""
from typing import Any
from .models import Booking
from .models import Tenant
from .booking_info import booking_email
from .filters import HostelFilter
from rooms_app.models import RoomProfile
from campus_app.models import CampusProfile
from hostel_app.models import HostelProfile

"""Built in Packages"""
from django.shortcuts import render
from django.views import generic
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import timedelta
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html')


class HostelListView(generic.ListView):
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        """Get hostel that are related to particular campus and display it
        to the client"""

        campus = CampusProfile.objects.get(
                campus_code=request.user.campus.campus_code
                )

        campus_hostels = HostelProfile.objects.filter(campus=campus)

        #context for the page
        context={'hostels':campus_hostels, 
                  'campus':campus, 
                  'myform': HostelFilter}

        return render(request, 'campus_hostels.html', context)


@login_required()
# allow strictly only POST
@require_http_methods(['POST'])
def book_room(request):     
    room_id = request.POST.get('room_id')
    room = RoomProfile.objects.get(room_id=room_id)
    bookings_count =Booking.objects.filter(room = room).count()
    number_left = room.room_capacity - bookings_count

    #check if room is full
    if  Booking.objects.filter(user=request.user, payed=False).exists():
        get_booking = Booking.objects.get(user = request.user)
        messages.info(request, 'Already Booked for a room please proceed to payment!!!')
        # print(request.META.get(''))    
        # return redirect(request.META.get('HTTP_REFERER'))
        return redirect('accounts:booking-and-payments')
    
    #check if tenant exits
    elif Tenant.objects.filter(user=request.user).exists():
        messages.info(request, 'Tenants can not book after payment')
        return redirect('accounts:booking-and-payments')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    #Creating booking for user
    else:
        student_id = request.user.student_id  
        booked_room = RoomProfile.objects.get(room_id=request.POST.get('room_id')) 
        #Saving booking info
        Book = Booking.objects.create(room=booked_room, user=request.user, 
                                      room_number=booked_room.room_no, hostel=booked_room.hostel, 
                                      student_id=student_id, status='Booked',
                                      end_time=(timezone.now() + timedelta(seconds=40)),
                                      campus=booked_room.campus).save()
        
        
        #redirect user for payment
        return redirect('accounts:booking-and-payments')
    
    
@login_required()
def delete_booking(request):

    try:
        booking = Booking.objects.get(user=request.user)
        booking.delete()
        
        #  delete any payment history id any
        from payments_app.models import PaymentHistory

        if PaymentHistory.objects.filter(user=request.user).exists():
            PaymentHistory.objects.get(user=request.user).delete()
            pass
        else:
            pass
        return redirect('accounts:booking-and-payments')
    
    except Booking.DoesNotExist:
        messages.info(request, 'No booking exits for this user')
        return redirect('accounts:booking-and-payments')


@login_required()
def search(request):
    search_data = request.GET['search_data']

    data = HostelFilter
    campus = CampusProfile.objects.get(campus_code=
                                       request.user.campus.campus_code)

    #query of search 
    query = HostelProfile.objects.filter(Q(campus=campus) & 
                                    (Q(hostel_name__icontains=search_data)
                                    | Q(location__icontains=search_data)))
    
    #context containg search query page
    context={'hostels':query, 
             'campus':campus,
             'myform': HostelFilter}
    
    return render(request, 'search.html', context)


@login_required()
def success_message(request):

    return render(request, 'successful.html')