from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from django.conf import settings

app_name ="maps"

time = settings.BOOKMIE_CACHING_TIMEOUT

urlpatterns = [
    path('hostel-direction/<str:hostel_code>/',cache_page(time)(views.hostel_direction), name="hostel-direction"),
    path('all-hostels/<str:campus_id>/',cache_page(time)(views.map_views), name='map-views'),
    path('guest-house-directions/<str:house_id>/', views.quick_room_direction, name='quick-room-direction')
    ]