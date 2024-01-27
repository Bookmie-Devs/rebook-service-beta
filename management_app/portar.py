from django.conf import settings
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render
from .models import Worker
from core.models import Tenant
from rooms_app.models import RoomProfile
from django.utils import timezone
from hostel_app.models import HostelProfile

def portar_office(request: HttpRequest):
    try:
        portar = Worker.objects.get(user=request.user)
        hostel = portar.hostel
        context={'user':request.user, 'hostel':hostel}
        return render(request, "portar_office.html",context)
    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")

def tenants(request: HttpRequest):
    try:
        portar = Worker.objects.get(user=request.user)
        hostel = portar.hostel
        all_active_tenants = Tenant.objects.filter(hostel=hostel, end_date__gt=timezone.now()).all()
        context={'tenants':all_active_tenants,'user':request.user}
        return render(request, "portar_htmx/",context)
    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")
    
def rooms(request: HttpRequest):
    try:
        portar = Worker.objects.get(user=request.user)
        hostel = portar.hostel
        rooms = RoomProfile.objects.filter(hostel=hostel).all()
        context={'rooms':rooms, 'user':request.user}
        return render(request, "portar_htmx/",context)
    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")

def profile(request: HttpRequest):
    try:
        portar = Worker.objects.get(user=request.user)
        hostel = portar.hostel
        context={'rooms':rooms, 'user':request.user}
        return render(request, "portar_htmx/",context)
    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")


def update_room_price(self, request:HttpRequest, *args, **kwargs):
    try:
        room_capacity = request.POST.get('room_capacity') #room with capacity
        new_price = request.POST.get('new_price') #price for those rooms
        hostel = HostelProfile.objects.get(hostel_manager=request.user)
        # check if room exist
        if RoomProfile.objects.filter(hostel=hostel, room_capacity=room_capacity).exists():
            rooms = RoomProfile.objects.filter(hostel=hostel, room_capacity=room_capacity)
            # calculate ptf_pricing 
            addtional_pricing: float = float(new_price) * settings.SUPPLY_COST_PERCENTAGE
            new_ptf_room_price = float(new_price) + float(addtional_pricing)

            rooms.update(room_price=new_price, ptf_room_price=new_ptf_room_price)
            return render({'message':'Rooms price have been updated'}, status=status.HTTP_201_CREATED)
        else: 
            return render({'message':'Rooms does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")




def edit_room(request: HttpRequest, room_id):
    context = {"message":None}
    try:
        portar = Worker.objects.get(user=request.user)
        room = RoomProfile.objects.get(room_id=room_id, hostel=portar.hostel)
        context.update({'portar':portar})
        if request.method=="POST":
            price = float(request.POST.get('price'))
            number_of_bed_spaces = int(request.POST.get('bed_space'))
            occupied = request.POST.get('occupied')
            room_number = request.POST.get('room_number')
            if RoomProfile.objects.filter(room_no=room_number).exists():
                context['message']="Room number already exist"
                return render(request, 'portar/htmx_message.html',context)
            context.update({"room":room})
        return render(request, 'portar/htmx_room_form.html',context)

    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")

