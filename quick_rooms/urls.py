from django.conf import settings
from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
time = settings.BOOKMIE_CACHING_TIMEOUT

app_name = 'quick-rooms'

urlpatterns = [
    path("secure-privacy-code/<room_id>/", views.request_code, name="secure-privacy-code"),
    path("generate-private-booking/", views.generate_private_booking, name="confirm-privacy"),
    path("book-room/", views.book_room, name="booking"),
    path("rooms/<campus_id>/", views.rooms , name="rooms"),
    path("profile/<booking_id>/", views.profile , name="profile"),
    path('privacy-policy/', (cache_page(time*5))(views.PrivacyPolicyView.as_view()), name='privacy-policy'),
]
