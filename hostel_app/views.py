from django.shortcuts import render, redirect
# from django
from django.http import HttpRequest
from django_google_maps.fields import GeoPt
from campus_app.models import CampusProfile
from .models import HostelProfile
from django.contrib.auth.decorators import login_required
from rooms_app.models import RoomProfile
from django.contrib import messages
from core.models import Booking


def hostel_profile(request, hostel_id):
    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)
    context = {'hostel': hostel_profile,'user':request.user}
    
    return render(request, 'hostel_profile.html', context)


def hostel_rooms(request: HttpRequest, hostel_id):
    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)
    # hostel coordinates on map
    coordinate:GeoPt = hostel_profile.geolocation 
    #get all unoccupied rooms in the hostel
    hostel_rooms = RoomProfile.objects.filter(hostel=hostel_profile, occupied=False).order_by('room_no')
    context:dict={'hostel':hostel_profile, 'hostel_rooms':hostel_rooms, 'user':request.user}
    # if user filter hostel rooms
    if request.GET: 
        rooms = RoomProfile.objects.filter(room_capacity=request.GET.get('capacity'), hostel=hostel_profile, occupied=False).all()
        if rooms.exists():
            context['hostel_rooms']=rooms
            return render(request, 'htmx_templates/htmx_hostel_rooms_filter.html', context)
        else:  
            context['hostel_rooms']=rooms
            return render(request, 'htmx_templates/htmx_hostel_rooms_filter.html', context)
        
    return render(request, 'hostel_rooms.html', context)

