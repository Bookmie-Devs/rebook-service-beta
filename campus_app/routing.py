
from django.urls import path
from django.views.decorators.cache import cache_page
from .views import CampusListView

app_name = 'campus'

urlpatterns = [
    path('campus-list/<str:router_value>/',cache_page(60 * 15)(CampusListView.as_view()), name='campus-list'),
]