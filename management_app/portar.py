from django.conf import settings
from django.http import HttpRequest, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from core.decorators import login_required_htmx
from django.shortcuts import redirect, render
from .models import Worker
from django.contrib import messages
from core.models import Tenant
from rooms_app.models import RoomProfile
from django.utils import timezone
from hostel_app.models import HostelProfile
from core.filters import PortarRoomFilters, PortarTenantFilters
from django.db.models import F
from django.contrib.auth.decorators import login_required

@login_required
def portar_office(request: HttpRequest):
    try:
        portar = Worker.objects.get(user=request.user)
        hostel = portar.hostel
        rooms = RoomProfile.objects.filter(hostel=hostel).all().order_by('room_no')
        all_active_tenants = Tenant.objects.filter(hostel=hostel, end_date__gt=timezone.now()).all()
        context={'user':request.user,'portar':portar, 'hostel':hostel,'rooms':rooms,'tenants':all_active_tenants,}
        return render(request, "management.html",context)
    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")

def filter_tenants(request: HttpRequest):
    try:
        capacity = request.GET.get('room_capacity')
        portar = Worker.objects.get(user=request.user)
        hostel = portar.hostel
        tenants = Tenant.objects.filter(hostel=hostel, end_date__gt=hostel.campus.end_of_acadamic_year)
        # tenants = Tenant.objects.filter(hostel=hostel,d=F('')l)
        filtered_tenants = PortarTenantFilters(request.GET, queryset=tenants).qs
        context={'tenants':filtered_tenants,'user':request.user}
        return render(request, "htmx_templates/management_htmx/htmx_tenant_filter.html/",context)
    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")

@login_required_htmx
@require_http_methods(['GET'])
def filter_rooms(request: HttpRequest):
    try:
        portar = Worker.objects.get(user=request.user)
        hostel = portar.hostel
        rooms = RoomProfile.objects.filter(hostel=hostel).all()
        filtered_roooms = PortarRoomFilters(request.GET, queryset=rooms,).qs
        context={'rooms':filtered_roooms, 'user':request.user}
        return render(request, "htmx_templates/management_htmx/htmx_room_filter.html",context)
    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")

@login_required_htmx
@require_http_methods(['GET'])
def search_rooms(request: HttpRequest):
    try:
        room_number = request.GET.get('room_number')
        portar = Worker.objects.get(user=request.user)
        hostel = portar.hostel
        rooms = RoomProfile.objects.filter(hostel=hostel,room_no__icontains=room_number)
        context={'rooms':rooms, 'user':request.user}
        return render(request, "htmx_templates/management_htmx/htmx_room_filter.html",context)
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


def update_room_price(request:HttpRequest, *args, **kwargs):
    context = {"message":None,"tag":None}
    try:
        if request.method=="POST":
            room_capacity = request.POST.get('room_cap') #room with capacity
            new_price = request.POST.get('new_price') #price for those rooms
            hostel = HostelProfile.objects.get(hostel_manager=request.user)
            # check if room exist
            if RoomProfile.objects.filter(hostel=hostel, room_capacity=room_capacity).exists():
                rooms = RoomProfile.objects.filter(hostel=hostel, room_capacity=room_capacity)
                # calculate ptf_pricing 
                addtional_pricing: float = float(new_price) * settings.SUPPLY_COST_PERCENTAGE
                new_ptf_room_price = float(new_price) + float(addtional_pricing)

                rooms.update(room_price=new_price, ptf_room_price=new_ptf_room_price)
                # context['message'] = 'Price updated'
                # print("hello")
                messages.info(request,"Price updated", extra_tags="success")
                return redirect("management:portar-office") 
            else:
                messages.info(request,"Room Capacity Doesn't Exist", extra_tags="danger")
                return redirect("management:portar-office") 
    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")




def edit_room(request: HttpRequest, room_id):
    context = {"message":None,"tag":None}
    try:
        portar = Worker.objects.get(user=request.user)
        room = RoomProfile.objects.get(room_id=room_id, hostel=portar.hostel)
        context.update({'portar':portar,"room":room})
        if request.method=="POST":
            price = float(request.POST.get('price'))
            number_of_bed_spaces = int(request.POST.get('bed_space'))
            occupied = request.POST.get('occupied')
            room_number = request.POST.get('room_number')
            room_capacity = request.POST.get('room_capacity')
            gender = request.POST.get('gender').lower()
            room.room_price=price
            room.room_capacity=room_capacity
            room.room_no=room_number
            room.bed_space_left=number_of_bed_spaces
            room.gender=gender
            # if occupied var returns None means checkbox was not checked
            # Therefore room was set to not occupied(False)
            if occupied==None:
                room.occupied=False
            else:
                # when checkbox is checked it is submited with a value of 1
                room.occupied=bool(int(occupied))
            room.save()
            context['tag']="success"
            context['message']="Room Has Been Updated"
            return render(request, 'htmx_templates/management_htmx/htmx_message.html',context)
        return render(request, 'htmx_templates/management_htmx/room_form.html',context)

    except Worker.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")


