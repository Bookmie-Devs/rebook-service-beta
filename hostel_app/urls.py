from django.urls import path
from . import api_views, views
from django.views.decorators.cache import cache_page
from django.conf import settings

app_name ='hostels' 

time = settings.BOOKMIE_CACHING_TIMEOUT

urlpatterns = [
    path('profile/<str:hostel_id>/',cache_page(time*3)(views.hostel_profile), name='profile'),
    path('hostel-rooms/<str:hostel_id>/', views.hostel_rooms, name='hostel-rooms'),
    
    # APIs
    path('api/profile/<str:hostel_id>/',api_views.HostelProfileView.as_view(), name='api-hostel-profile'),
    path('api/hostel-rooms/<str:hostel_id>/',api_views.HostelRoomsView.as_view(), name='api-hostel-rooms'),
]