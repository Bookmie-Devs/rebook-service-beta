from django.http import HttpRequest
from .models import Worker
from core.models import Tenant
from django.utils import timezone
from hostel_app.models import HostelProfile

def tenants(request: HttpRequest):
    portar = Worker.objects.get(user=request.user)
    hostel = HostelProfile.objects.get(hostel=portar.hostel)
    all_active_tenants = Tenant.objects.filter(hostel=hostel, end_date__lt=timezone.now())




