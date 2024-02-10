from django.shortcuts import render
from django_google_maps.fields import GeoPt
from campus_app.models import CampusProfile, CollegeProfile
from hostel_app.models import HostelProfile

def hostel_direction(request, hostel_id):
    hostel_profile = HostelProfile.objects.get(hostel_id = hostel_id)
    # hostel coordinates on map
    coordinate:GeoPt = hostel_profile.geolocation
    # coordinate of campus
    campus_coordinates: GeoPt = hostel_profile.campus.geolocation
    colleges = CollegeProfile.objects.filter(campus_name=hostel_profile.campus).all()
    college_coordinates = [{'coordinate':{'lat':college.geolocation.lat, 'lng':college.geolocation.lon,}, 'name':college.college_name} for college in colleges]
    return render(request=request,
           template_name= 'maps/map_direction.html/',
           context={'coordinate': coordinate,"campus_coordinates":campus_coordinates ,'user':request.user ,'hostel':hostel_profile, 'colleges':college_coordinates})


def map_views(request, campus_id):
    campus = CampusProfile.objects.get(campus_id=campus_id)
    hostel_profiles = HostelProfile.objects.filter(verified=True,campus=campus).all()
    colleges = CollegeProfile.objects.filter(campus_name=campus).all()
    # # hostel coordinates on map
    # coordinatet = hostel_profile.geolocation
    # coordinate. 
    coordinates:GeoPt= [{'lat': hostel.geolocation.lat, 'lng': hostel.geolocation.lon, 'url':f'/hostels/profile/{hostel.hostel_id}/','name':hostel.hostel_name.title()} for hostel in hostel_profiles]
    college_coordinates = [{'coordinate':{'lat':college.geolocation.lat, 'lng':college.geolocation.lon,}, 'name':college.college_name} for college in colleges]
    # return render(request, 'your_template.html', })
    return render(request=request,
           template_name= 'maps/map_views.html/',
           context={'coordinates': coordinates,'campus':campus, 'colleges':college_coordinates})