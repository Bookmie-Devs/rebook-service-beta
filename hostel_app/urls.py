from django.urls import path
from . import views

app_name ='HostelApp' 

urlpatterns = [
    path('profile/<str:pk_hostel>/',views.hostelProfile, name='hostelProfile'),
    path('HostelRooms/<str:pk_HostelName>/', views.HostelRooms, name='HostelRooms'),
    path('filter_rooms/<int:filter_opt>/<str:hostelName>/', views.filter_rooms_in_hostel, name='filter_hostel_rooms')
]