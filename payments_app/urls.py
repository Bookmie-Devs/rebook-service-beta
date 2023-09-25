from django.urls import path
from . import views

app_name = 'PaymentApp'
urlpatterns = [
    path('payment/<str:room_id>/', views.initiate_payment, name='init_payment'),
    path('verify-payments/<reference>', views.verify_payment_success, name="verify_payments")
]