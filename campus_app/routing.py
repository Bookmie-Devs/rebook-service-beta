
from django.urls import path

from .views import CampusListView

app_name = 'campus'

urlpatterns = [
    path('campus-list/<str:router_value>/', CampusListView.as_view(), name='campus-list'),
]