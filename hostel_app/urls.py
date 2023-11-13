from django.urls import path
from . import api_views, views

app_name ='hostels' 

urlpatterns = [
    path('profile/<str:hostel_id>/',views.hostel_profile, name='profile'),
    path('hostel-rooms/<str:hostel_id>/', views.hostel_rooms, name='hostel-rooms'),
    path('filter_rooms/', views.filter_rooms, name='filter-rooms'),

    # APIs
    path('api/profile/<str:hostel_id>/',api_views.HostelProfileView.as_view(), name='api-hostel-profile'),
    path('api/hostel-rooms/<str:hostel_id>/',api_views.HostelRoomsView.as_view(), name='api-hostel-rooms'),
]