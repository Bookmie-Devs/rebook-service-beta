from django.shortcuts import render, redirect
from hostel_app.models import HostelProfile
from .models import RoomProfile
from core.models import Booking
from core.models import CustomUser
from core.filters import RoomFilters
from campus_app.models import CampusProfile
from .models import RoomForSale
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from campus_app.models import CampusProfile

@login_required(login_url='Core:login')
def room_profile(request, room_id):
    room = RoomProfile.objects.get(room_id=room_id)
    room_bookers = Booking.objects.filter(Room=room).all()
    return render(request, 'RoomProfile.html', {'Room':room, 'room_bookers':room_bookers})
CustomUser.campus
@login_required(login_url='Core:login')
def All_available_rooms(request, filter_opt):
    CampusProfile.Campus_ID
    campus = CampusProfile.objects.get(Campus_ID=request.user.campus)
    # HostelPro = HostelProfile.objects.get(HostelName = pk_HostelName)
    Hostel_rooms = RoomProfile.objects.filter(Occupied=False)
    # RoomProfile.
    # Campus = HostelPro.Campus_of_Hostel
    context ={
        # 'HostelPro':HostelPro,
        'Hostel_rooms':Hostel_rooms, }
        # 'Campus':Campus}
    return render(request, 'Rooms.html', context)

@login_required(login_url='Core:login')
def sell_room(request, room_id):
    if request.method=='POST':     
        price = request.POST['price']
        if RoomProfile.objects.filter(Room_ID=room_id).exists():
            get_room = RoomProfile.objects.get(Room_ID=room_id)
            save_sell = RoomForSale.objects.create(user=request.user, Username=request.user.username, Room=get_room,
                                               Hostel=get_room.Hostel, newPrice=price, Valid=True,)
            save_sell.save()
        else:
            messages.info(request, 'Room does not exist')
            return redirect()


@login_required(login_url='Core:login')
def campus_filter_of_rooms(request):
    all_rooms = RoomProfile.objects.all()

    print(request.POST)
    search = RoomFilters(request.POST, queryset=all_rooms)
    query_set = search.qs
    get_campus = request.user.campus
    # if get_rooms.exists():
    return render(request, 'filter_rooms.html', {'get_rooms': query_set,'Campus':get_campus, 'myForm':RoomFilters})
    
    # else:  
    #     messages.info(request, f"All {filter_opt}'s a in room are full")
    #     return render(request, 'filter_rooms.html', {'get_rooms':get_rooms,'Campus':get_campus})
    











