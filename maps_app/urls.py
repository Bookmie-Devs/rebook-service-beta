from django.urls import path
from . import views

app_name ="maps"

urlpatterns = [
    path('hostel-map-direction/<str:hostel_id>/', views.location_direction, name="hostel-direction")]