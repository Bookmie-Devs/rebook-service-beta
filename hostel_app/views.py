# Create your views here.
from django.shortcuts import render, redirect
from .models import HostelProfile
from django.contrib.auth.decorators import login_required
from rooms_app.models import RoomProfile
from django.contrib import messages
from core.models import Booking

def hostelProfile(request, pk_hostel):
    HostelPro = HostelProfile.objects.get(HostelName = pk_hostel)
    Hostel_rooms = RoomProfile.objects.filter(Hostel = HostelPro, Occupied=False)

    Campus = HostelPro.Campus_of_Hostel
    context = {'HostelPro': HostelPro,
               'Campus': Campus,
               'Hostel_rooms':Hostel_rooms,}
    return render(request, 'HostelProfile.html', context)

@login_required(login_url='Core:login')
def HostelRooms(request, pk_HostelName):
    # HostelProfile.Occupied
    HostelPro = HostelProfile.objects.get(HostelName = pk_HostelName)
    Hostel_rooms = RoomProfile.objects.filter(Hostel=HostelPro, Occupied=False)
    # full = bookings_count == Hostel_rooms.
    Campus = HostelPro.Campus_of_Hostel
    context ={
        'user':request.user,
        'HostelPro':HostelPro,
        'Hostel_rooms':Hostel_rooms, 
        'Campus':Campus}
    return render(request, 'HostelRooms.html', context)


@login_required(login_url='Core:login')
def filter_rooms_in_hostel(request, filter_opt, hostelName):
    get_campus = request.user.campus
    get_hostel = HostelProfile.objects.get(HostelName=hostelName)
    get_rooms = RoomProfile.objects.filter(Room_Capacity=filter_opt, Hostel=get_hostel, Occupied=False)
    if get_rooms.exists():
        context = {'HostelPro': get_hostel,
                   'Campus': get_campus,
                   'Hostel_rooms':get_rooms,}
        return render(request, 'HostelRooms.html', context)
    
    else:  
        context = {'HostelPro': get_hostel,
                   'Campus': get_campus,
                   'Hostel_rooms':get_rooms,}
        messages.info(request, f"All {filter_opt} in a room are full")
        return render(request, 'HostelRooms.html', context)
    