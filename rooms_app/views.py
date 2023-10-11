from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse

from hostel_app.models import HostelProfile
from .models import RoomProfile
from core.models import Booking
from core.models import CustomUser
from core.filters import RoomFilters
from campus_app.models import CampusProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from campus_app.models import CampusProfile

@login_required()
def room_profile(request, room_id):
    room = RoomProfile.objects.get(room_id=room_id)
    room_bookers = Booking.objects.filter(room=room).all()
    return render(request, 'room_profile.html', {'room':room, 'room_bookers':room_bookers})


@login_required()
def filter_of_rooms(request):
    all_rooms = RoomProfile.objects.filter(campus=request.user.campus, occupied=False).all()
    all_hostels = HostelProfile.objects.all()
    search = RoomFilters(request.GET, queryset=all_rooms)
    query_set = search.qs
    get_campus = request.user.campus

    context = {'rooms': query_set,'Campus':get_campus, 
               'hostels':all_hostels,'myForm':RoomFilters}
    
    if request.GET:
        if query_set.exists():
            messages.info(request, "Scroll down for results")
            return render(request,  'filter_rooms.html', context)
        
        else:
            messages.info(request, "No rooms with such details available")
            # return redirect('rooms:filter-rooms')
            return render(request,  'filter_rooms.html',)
        
    return render(request,  'filter_rooms.html', context)








