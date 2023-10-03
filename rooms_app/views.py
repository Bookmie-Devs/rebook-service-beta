from django.shortcuts import render, redirect
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
    return render(request, 'RoomProfile.html', {'Room':room, 'room_bookers':room_bookers})



@login_required()
def all_available_rooms(request, filter_opt):
    CampusProfile.Campus_ID
    campus = CampusProfile.objects.get(Campus_ID=request.user.campus)
    # HostelPro = HostelProfile.objects.get(HostelName = pk_HostelName)
    Hostel_rooms = RoomProfile.objects.filter(Occupied=False)
    # RoomProfile.
    # Campus = HostelPro.Campus_of_Hostel
    context ={
        # 'HostelPro':HostelPro,
        'Hostel_rooms':Hostel_rooms,}
        # 'Campus':Campus}
    return render(request, 'Rooms.html', context)



@login_required()
def filter_of_rooms(request):
    all_rooms = RoomProfile.objects.filter(campus=request.user.campus).all()
    all_hostels = HostelProfile.objects.all()
    search = RoomFilters(request.GET, queryset=all_rooms)
    query_set = search.qs
    get_campus = request.user.campus
    if query_set.exists():
        return render(request,  'filter_rooms.html', 
                                {'get_rooms': query_set,
                                'Campus':get_campus, 
                                'hostels':all_hostels,
                                'myForm':RoomFilters})
    else:  
        messages.info(request, "No rooms with such details available")
        return redirect('rooms:filter-rooms')
    











