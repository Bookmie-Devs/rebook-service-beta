from django.shortcuts import render
from django_google_maps.fields import GeoPt
from hostel_app.models import HostelProfile

def hostel_direction(request, hostel_id):
    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)
    # hostel coordinates on map
    coordinate:GeoPt = hostel_profile.geolocation
    # coordinate. 
    return render(request=request,
           template_name= 'maps/map_direction.html/',
           context={'coordinate': coordinate, 'user':request.user ,'hostel':hostel_profile})


def map_views(request):
    hostel_profiles = HostelProfile.objects.all()
    # # hostel coordinates on map
    # coordinatet = hostel_profile.geolocation
    # coordinate. 
    coordinates:GeoPt= [{'lat': profile.geolocation.lat, 'lng': profile.geolocation.lon, 'url':f'/hostels/profile/{profile.hostel_id}/'} for profile in hostel_profiles]

    # return render(request, 'your_template.html', })
    return render(request=request,
           template_name= 'maps/map_views.html/',
           context={'coordinates': coordinates})