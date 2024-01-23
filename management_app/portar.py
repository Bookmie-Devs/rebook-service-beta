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




