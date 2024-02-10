from django.urls import path
from . import views
from . import portar
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView


app_name='management'

urlpatterns=[
    path('obtain-token/', TokenObtainPairView.as_view(), name=''),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('request-otp-phone/', views.get_otp_phone, name='request-otp-phone'),
    path('confirm-otp-phone/', views.confirm_otp_phone, name='confirm-otp-phone'),

    path('management-profile/', views.HostelProfileView.as_view(),name='hostel-profile-view'),
    path('sales-stats/', views.SalesStatsView.as_view(), name="sales-stats"),
    path('update-room-price/', views.UpdateRoomPrice.as_view(), name='change-price'),
                                                
    path('rooms/', views.RoomListView.as_view(), name='get-rooms'),
    path('room-details/<str:room_id>/', views.RoomDetailView.as_view(), name="room-details"),
    path('verify-tenant/', views.verify_tenant, name='verify-tenant'),
    path('view-tenants/', views.TenantListView.as_view(), name='view-tenants'),

    path("portar-office/", portar.portar_office, name="portar-office"),
    path("portar-office/filter-rooms/", portar.filter_rooms, name="portar-filter-rooms"),
    path("portar-office/search-rooms/", portar.search_rooms, name="portar-search-rooms"),
    path("portar-office/filter-tenants/", portar.filter_tenants, name="portar-filter-tenants"),
    path("portar-office/edit-room/<str:room_id>/", portar.edit_room , name="portar-edit-room"),
    path("portar-office/update-prices/", portar.update_room_price, name="portar-update-prices"),
]
