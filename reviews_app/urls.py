from django.urls import path
from .views import feedback_message, customer_care

app_name = "reviews"

urlpatterns = [
    path("feedback-and-issues/",feedback_message, name="feedback"),
    path("customer-care/", customer_care, name="customer-care")
]