# Create your views here.
from django.shortcuts import render, redirect
from .models import HostelProfile
from django.contrib.auth.decorators import login_required
from rooms_app.models import RoomProfile
from django.contrib import messages
from core.models import Booking

@login_required()
def hostel_profile(request, hostel_id):
    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)

    context = {'hostel': hostel_profile,
               'Campus': hostel_profile.campus,}
    
    return render(request, 'hostel_profile.html', context)


@login_required()
def hostel_rooms(request, hostel_id):

    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)
    
    #get all unoccupied rooms in the hostel
    hostel_rooms = RoomProfile.objects.filter(hostel=hostel_profile, occupied=False).order_by('room_no')

    context ={'user':request.user,
            'hostel':hostel_profile,
            'hostel_rooms':hostel_rooms, 
            'campus':hostel_profile.campus}
    
    return render(request, 'hostel_rooms.html', context)


@login_required()
def filter_rooms(request):

    campus = request.user.campus
    hostel = HostelProfile.objects.get(hostel_id=request.GET.get('hostel'))

    #query rooms per requirements
    rooms = RoomProfile.objects.filter(room_capacity=request.GET.get('capacity'), hostel=hostel, occupied=False).all()

    if rooms.exists():
        context = {'hostel': hostel,
                   'campus': campus,
                   'hostel_rooms':rooms,}
        return render(request, 'hostel_rooms.html', context)
    
    else:  
        context = {'hostel': hostel,
                   'campus': campus,
                   'hostel_rooms':rooms,}
        return render(request, 'hostel_rooms.html', context)
    