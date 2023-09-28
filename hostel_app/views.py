# Create your views here.
from django.shortcuts import render, redirect
from .models import HostelProfile
from django.contrib.auth.decorators import login_required
from rooms_app.models import RoomProfile
from django.contrib import messages
from core.models import Booking

def hostel_profile(request, hostel_id):
    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)
    rooms = RoomProfile.objects.filter(Hostel=hostel_profile, Occupied=False)

    campus = hostel_profile.campus
    context = {'hostel_profile': hostel_profile,
               'Campus': campus,
               'Hostel_rooms':rooms,}
    return render(request, 'HostelProfile.html', context)


@login_required(login_url='accounts:login')
def hostel_rooms(request, hostel_id):

    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)
    
    #get all unoccupied rooms in the hostel
    hostel_rooms = RoomProfile.objects.filter(hostel=hostel_profile, occupied=False)

    context ={'user':request.user,
            'hostel':hostel_profile,
            'hostel_rooms':hostel_rooms, 
            'campus':hostel_profile.campus}
    
    return render(request, 'hostel_rooms.html', context)


@login_required(login_url='Core:login')
def filter_rooms(request, capacity, hostel_id):

    campus = request.user.campus
    hostel = HostelProfile.objects.get(hostel_id=hostel_id)

    #query rooms per requirements
    rooms = RoomProfile.objects.filter(room_capacity=capacity, hostel=hostel, occupied=False)

    if rooms.exists():
        context = {'hostel': hostel,
                   'campus': campus,
                   'hostel_rooms':rooms,}
        return render(request, 'hostel_rooms.html', context)
    
    else:  
        context = {'hostel': hostel,
                   'campus': campus,
                   'hostel_rooms':rooms,}
        messages.info(request, f"All {capacity} in a room are full")
        return render(request, 'hostel_rooms.html', context)
    