from django.urls import path
from . import views

app_name ="maps"

urlpatterns = [
    path('hostel-direction/<str:hostel_id>/', views.hostel_direction, name="hostel-direction"),
    path('all-hostels/', views.map_views, name='map-views')
    ]