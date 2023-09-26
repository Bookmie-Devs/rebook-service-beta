from django.urls import path
from . import views

app_name = 'rooms'
urlpatterns = [
    path('view_rooms/<str:filter_opt>/<str:hostelName>/', views.all_available_rooms, name='filter_all_rooms'),
    path('profile/<str:room_id>/', views.room_profile, name='profile' ),
    path('filter-rooms/', views.filter_of_rooms, name='filter-rooms')]