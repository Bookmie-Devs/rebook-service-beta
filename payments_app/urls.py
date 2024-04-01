from django.urls import path
from .part_payments import initiate_part_payment, verify_complete_payment, complete_part_payment
from . import views
from . import physical_payment
from quick_rooms.views import verify_quick_room_payment

app_name = 'payments'
urlpatterns = [
    path('init-payment/<str:room_id>/', views.initiate_payment, name='init-payment'),
    path('init-part-payment/<str:room_id>/', initiate_part_payment, name='init-part-payment'),
    path('make-payment/<str:reference_id>/<str:room_id>/', views.make_payment, name='make-payment'),
    path('complete-part-payment/', complete_part_payment, name='complete-part-payment'),
    path('verify-payment/<str:reference_id>/<paystack_reference>/', views.verify_payment, name="verify-payment"),
    path('verify-complete-payment/<str:reference_id>/<paystack_reference>/', verify_complete_payment, name="verify-complete-payment"),
    path('quick-room-payment-verification/<str:reference_id>/<paystack_reference>/', verify_quick_room_payment, name="verify-quick-room-payment"),
    path('tenant-authentication/', views.tenant_auth, name='tenant-authentication'),

    # physical payments
    path('physical-payments/', physical_payment.physical_payment, name='physical-init'),
    path("physical-payments/payment_id/", physical_payment.physical_payment_confirm, name="physical-payment-confirm"),
    path('physical-payments/verification/', physical_payment.generate_physical_payemnt_details, name='generate-details')
]