from django.urls import path
from . import views

app_name = 'rooms'
urlpatterns = [
    path('view_rooms/<str:filter_opt>/<str:hostelName>/', views.All_available_rooms, name='filter_all_rooms'),
    path('profile/<str:room_id>/', views.room_profile, name='room_profile' ),
    path('filter_rooms/', views.campus_filter_of_rooms, name='filter_rooms')]