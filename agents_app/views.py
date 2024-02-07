from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render
from agents_app.models import HostelAgent
from hostel_app.models import HostelProfile
# Create your views here.
HostelProfile.agent_affiliate
def agent_admin(request: HttpRequest):
    try:
        agent = HostelAgent.objects.get(user=request.user, is_verified=True, is_active=True)
        all_agent_hostels = HostelProfile.objects.filter(agent_affiliate=agent).all()
        pass
    except HostelAgent.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page")  