from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "accounts"
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('booking-and-payments/', views.booking_and_payments, name='booking-and-payments'),
    
    # Apis
    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/refresh-token/', TokenRefreshView.as_view(),name='api-refresh-token'),
    ]
  