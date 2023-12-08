
from django.urls import path
from django.views.decorators.cache import cache_page
from .views import CampusListView
from django.conf import settings

app_name = 'campus'

time = settings.BOOKMIE_CACHING_TIMEOUT

urlpatterns = [
    path('campus-list/<str:router_value>/',cache_page(time)(CampusListView.as_view()), name='campus-list'),
]