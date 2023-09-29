from django.utils import timezone
from django.utils.timezone import timedelta
from django.shortcuts import render

from django.shortcuts import redirect
from rooms_app.models import RoomProfile
from campus_app.models import CampusProfile
from hostel_app.models import HostelProfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Booking
from django.conf import settings
from .filters import HostelFilter
from .models import Tenant


from .filters import HostelFilter
from django.shortcuts import render
from .booking_info import booking_email


def index(request):
    return render(request, 'index.html')


@login_required(login_url='accounts:login')
def hostels(request):
    
    """Get hostel that are related to particular campus and display it
    to the client"""
    campus = CampusProfile.objects.get(campus_code=
                                       request.user.campus.campus_code)
    
    campus_hostels = HostelProfile.objects.filter(campus=campus)

    #context for the page
    context={'hostels':campus_hostels, 
              'campus':campus, 'myform': HostelFilter}
    
    return render(request, 'campus_hostels.html', context)


@login_required(login_url='accounts:login')
def book_room(request, room_id):
    room = RoomProfile.objects.get(room_id=room_id)
    bookings_count =Booking.objects.filter(room = room).count()
    number_left = room.room_capacity - bookings_count

    if request.method == 'POST':
    #check if room is full
        if  Booking.objects.filter(user=request.user, payed=False).exists():
            get_booking = Booking.objects.get(user = request.user)
            messages.info(request, 'Already Booked for a room please proceed to payment!!!')
            return redirect('payments:make-payment', get_booking.room.room_id)
        
        #check if tenant exits
        elif Tenant.objects.filter(user=request.user).exists():
            messages.info(request, 'You already payed for a room')
            return redirect('hostels:hostel-rooms', hostel_id=room.hostel.hostel_id)

        #Checking if room is full
        elif bookings_count >= room.room_capacity:
            messages.info(request, 'Room if full for booking try again in 24 hrs')
            return redirect('hostels:hostel_rooms', hostel_id=room.hostel.hostel_id)

        #Creating booking for user
        else:
            student_id = request.user.student_id  
            booked_room = RoomProfile.objects.get(room_id=request.POST.get('room_id')) 
            #Saving booking info
            Book = Booking.objects.create(room=booked_room, user=request.user, room_number=booked_room.room_no, hostel=booked_room.hostel, 
                student_id=student_id, status='Booked', end_time=(timezone.now() + timedelta(seconds=40)), campus=booked_room.campus).save()

            if bookings_count == room.room_capacity:
                room.occupied=True
                room.save()
                pass
            
            #send email to user
            booking_email(user=request.user,booking_id=Booking.booking_id,
                          EMAIL_HOST_USER=settings.EMAIL_HOST_USER)
            
            #redirect user for payment
            return redirect('payments:init-payment', room_id=room.room_id )
    

def search(request):
    all_hotels = HostelProfile.objects.all()
    search_data = HostelFilter(request.POST, queryset=all_hotels)
    query =HostelProfile.objects.filter(hostel_name__icontains=request.POST['search_data']).all()

    campus = CampusProfile.objects.get(campus_code=
                                       request.user.campus.campus_code)
    
    campus_hostels = HostelProfile.objects.filter(campus=campus)

    #context containg search query page
    context={'hostels':query, 
              'campus':campus, 'myform': HostelFilter}
    
    return render(request, 'search.html', context)

