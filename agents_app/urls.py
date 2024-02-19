from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path("agent-hostels/", views.agent_hostels , name="agent-hostels"),
    path("agent-rooms/", views.agent_rooms , name="agent-rooms"),
    path("agent-rooms/<room_id>/", views.agent_room_profile , name="agent-room=-profile"),
    path("agent-hostels/<hostel_id>/", views.agent_hostel_profile , name="agent-hostel-profile"),
]

