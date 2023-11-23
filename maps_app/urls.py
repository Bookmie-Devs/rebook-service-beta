from django.urls import path
from . import views

app_name ="maps"

urlpatterns = [
    path('hostel-direction/<str:hostel_id>/', views.location_direction, name="hostel-direction")]