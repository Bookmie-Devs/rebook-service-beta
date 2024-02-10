from django.urls import path
from .views import feedback_message, customer_care, like_hostel
from .views import feedback_message, customer_care, news_letter, ContactView
from django.views.decorators.cache import cache_page
from django.conf import settings

time = settings.BOOKMIE_CACHING_TIMEOUT

app_name = "reviews"

urlpatterns = [
    path("feedback-and-issues/",feedback_message, name="feedback"),
    path("customer-care/", customer_care, name="customer-care"),
    path("like-hostel/",like_hostel,name="like-hostel"),
    path('news-letter/', news_letter, name="news-letter"),
    path('contact/',(cache_page(time*5))(ContactView.as_view()), name='contact'),
]