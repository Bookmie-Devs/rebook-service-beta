from django.urls import path
from . import views

app_name = 'payments'
urlpatterns = [
    path('init-payment/<str:room_id>/', views.initiate_payment, name='init-payment'),
    path('make-payment/<str:room_id>/', views.make_payment, name='make-payment'),
    path('verify-payment/', views.verify_payment, name="verify-payment"),
    path('tenant-authentication/', views.tenant_auth, name='tenant-authentication')
]