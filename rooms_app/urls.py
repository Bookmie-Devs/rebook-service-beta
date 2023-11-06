from django.urls import path
from . import views

app_name = 'rooms'
urlpatterns = [
    path('room-profile/<str:room_id>/', views.room_profile, name='profile' ),
    path('campus-rooms/<str:campus_code>/', views.CampusRoomListView.as_view(), name='campus-rooms')
    ]