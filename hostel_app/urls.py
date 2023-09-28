from django.urls import path
from . import views

app_name ='hostels' 

urlpatterns = [
    path('profile/<str:hostel_id>/',views.hostel_profile, name='profile'),
    path('hostel-rooms/<str:hostel_id>/', views.hostel_rooms, name='hostel-rooms'),
    path('filter_rooms/<int:capacity>/<str:hostel_id>/', views.filter_rooms, name='filter-rooms')
]