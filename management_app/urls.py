from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView


app_name='management'

urlpatterns=[
    path('obtain-token/', TokenObtainPairView.as_view(), name=''),
    path('change-price/', views.change_room_price, name='change-price'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('hostel-profile/<str:host_code>/', views.HostelProfileView.as_view(),
                                                name='hostel-profile-view'),
                                                
    path('rooms/', views.get_rooms, name='get-rooms'),
    path('room-details/<str:room_id>', views.RoomDetailView.as_view(), name="room-details"),
    path('verify-tenant/', views.verify_tenant, name='verify-tenant'),
    path('verify-booking/', views.get_booking, name='verify-booking'),
    # path('veiw-tanants/', views.view_tenants, name='view-tenants')
]
