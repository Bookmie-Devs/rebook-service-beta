# Create your views here.
from django.shortcuts import render, redirect
from .models import HostelProfile
from django.contrib.auth.decorators import login_required
from rooms_app.models import RoomProfile
from django.contrib import messages
from core.models import Booking

def hostel_profile(request, hostel_id):
    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)
    Hostel_rooms = RoomProfile.objects.filter(Hostel = hostel_profile, Occupied=False)

    Campus = hostel_profile.campus
    context = {'hostel_profile': hostel_profile,
               'Campus': Campus,
               'Hostel_rooms':Hostel_rooms,}
    return render(request, 'HostelProfile.html', context)

@login_required(login_url='accounts:login')
def hostel_rooms(request, hostel_id):
    # HostelProfile.Occupied
    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)
    hostel_rooms = RoomProfile.objects.filter(hostel=hostel_profile, occupied=False)
    # full = bookings_count == Hostel_rooms.
    campus = hostel_profile.campus
    context ={
        'user':request.user,
        'hostel':hostel_profile,
        'hostel_rooms':hostel_rooms, 
        'Campus':campus}
    return render(request, 'hostel_rooms.html', context)


@login_required(login_url='Core:login')
def filter_rooms_in_hostel(request, filter_opt, hostelName):
    get_campus = request.user.campus
    get_hostel = HostelProfile.objects.get(HostelName=hostelName)
    get_rooms = RoomProfile.objects.filter(Room_Capacity=filter_opt, Hostel=get_hostel, Occupied=False)
    if get_rooms.exists():
        context = {'hostel_profile': get_hostel,
                   'Campus': get_campus,
                   'Hostel_rooms':get_rooms,}
        return render(request, 'HostelRooms.html', context)
    
    else:  
        context = {'hostel_profile': get_hostel,
                   'Campus': get_campus,
                   'Hostel_rooms':get_rooms,}
        messages.info(request, f"All {filter_opt} in a room are full")
        return render(request, 'HostelRooms.html', context)
    