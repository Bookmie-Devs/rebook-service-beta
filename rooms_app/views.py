from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse

from hostel_app.models import HostelProfile
from .models import RoomProfile
from core.models import Booking
from core.models import CustomUser
from django.views import generic
from core.filters import RoomFilters
from campus_app.models import CampusProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from campus_app.models import CampusProfile

# room details
def room_profile(request, room_id):
    room = RoomProfile.objects.get(room_id=room_id)
    # room_bookers = Booking.objects.filter(room=room).all()
    return render(request, 'room_profile.html', {'room':room,})



"""when user clicks on a campus card"""
class CampusRoomListView(generic.ListView):
    def get(self, request: HttpRequest, campus_param_id:str ,*args: Any, **kwargs: Any) -> HttpResponse:
        # get campus code
        campus = CampusProfile.objects.get(campus_param_id = campus_param_id)
        # Use if we expand to other campuses
        campus_rooms = RoomProfile.objects.filter(campus=campus, occupied=False, verified=True).all()
        # context for all pages if no search is return or
        # if there no qs for search data 
        context = {'rooms': campus_rooms, 'campus':campus, 'user':request.user,}        
        if request.GET:
            # Search query
            search = RoomFilters(request.GET, queryset=campus_rooms)
            query_set = search.qs
            # set rooms to seerch results after search
            context['rooms'] = query_set
            if query_set.exists():
                return render(request,  'htmx_templates/htmx_campus_rooms_filter.html', context)
            # include context to let template have access
            # to campus code for routing back
            # else an error will generated(code = 500)
            else:
                return render(request,  'htmx_templates/htmx_campus_rooms_filter.html', context)
            
        return render(request,  'campus_rooms.html', context)









