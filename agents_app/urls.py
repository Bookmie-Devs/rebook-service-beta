from django.urls import path
from . import views

urlpatterns = [
    path("agent-admin", views.agent_admin , name="agent-admin")
]
