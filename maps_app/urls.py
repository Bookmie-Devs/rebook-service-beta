from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
app_name ="maps"

urlpatterns = [
    path('hostel-direction/<str:hostel_id>/',cache_page(60 * 15)(views.hostel_direction), name="hostel-direction"),
    path('all-hostels/',cache_page(60 * 15)(views.map_views), name='map-views')
    ]