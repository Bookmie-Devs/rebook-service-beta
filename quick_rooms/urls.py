from django.urls import path
from . import views


app_name = 'quick-rooms'

urlpatterns = [
    path("quick-privacy/", views.quick_room_login , name="quick-privacy"),
    path("confirm-privacy-code/", views.confirm_code, name="confirm-privacy"),
    path("rooms/", views.quick_room_login , name="rooms")
]
