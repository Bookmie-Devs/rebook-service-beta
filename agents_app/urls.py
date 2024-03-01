from django.urls import path
from . import views
from . import management

app_name = 'agents'

urlpatterns = [
    path('request-office-otp/', management.get_otp_phone, name='request-office-otp'),
    path("agent-registered-hostels/", views.agent_hostels , name="agent-hostels"),
    path("agent-registered-rooms/", views.agent_registered_rooms , name="agent-rooms"),
    path("agent-registered-rooms/<room_id>/", views.RoomProfileView.as_view() , name="agent-room=-profile"),
    path("agent-registered-hostels/<hostel_id>/", views.agent_hostel_profile , name="agent-hostel-profile"),
    path("register-hostel/", views.HostelProfileView.as_view(), name="register-hostel"),
]

