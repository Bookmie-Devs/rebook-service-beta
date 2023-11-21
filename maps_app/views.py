from django.shortcuts import render
from django_google_maps.fields import GeoPt
from hostel_app.models import HostelProfile

def location_direction(request, hostel_id):
    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)
    # hostel coordinates on map
    coordinate:GeoPt = hostel_profile.geolocation
    # coordinate. 
    return render(request=request,
           template_name= 'maps/map_direction.html/',
           context={'coordinate': coordinate, 'hostel':hostel_profile})