from django.urls import path
from . import views
from . import portar
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView


app_name='management'

urlpatterns=[
    path('obtain-token/', TokenObtainPairView.as_view(), name=''),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),

    path('management-profile/', views.HostelProfileView.as_view(),name='hostel-profile-view'),
    path('sales-stats/', views.SalesStatsView.as_view(), name="sales-stats"),
    path('update-room-price/', views.UpdateRoomPrice.as_view(), name='change-price'),
                                                
    path('rooms/', views.RoomListView.as_view(), name='get-rooms'),
    path('room-details/<str:room_id>/', views.RoomDetailView.as_view(), name="room-details"),
    path('verify-tenant/', views.verify_tenant, name='verify-tenant'),
    path('view-tenants/', views.TenantListView.as_view(), name='view-tenants'),

    path("portar-office/", portar.portar_office, name="portar-office"),
    path("portar-office/rooms/", portar.rooms , name="portar-office-rooms"),
    path("portar-office/tenants/", portar.tenants, name="portar-office-tenants"),
]
