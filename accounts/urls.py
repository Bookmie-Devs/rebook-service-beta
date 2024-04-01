from django.urls import path
from . import views
from . import api_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "accounts"
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate_account'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path("complete-profile/<user_uuid>/", views.complete_profile, name="complete-profile"),
    path('booking-and-payments/', views.booking_and_payments, name='booking-and-payments'),
    
    # Apis
    path('api/login/', TokenObtainPairView.as_view(), name='login-api'),
    path('api/refresh-token/', TokenRefreshView.as_view(),name='refresh-token-api'),
    path('api/signup/',api_views.signup_api_view,name='signup-api'),
    path('api/booking-and-payments/', views.booking_and_payments, name='booking-and-payments-api'),
    ]
  