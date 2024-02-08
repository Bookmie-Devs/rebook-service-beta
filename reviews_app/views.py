from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from hostel_app.models import HostelProfile
from rooms_app.models import RoomProfile
from .models import FeedBackMessage, CustomerCare, HostelLike, RoomLike
from core.decorators import login_required_htmx
from django.http import (HttpRequest, 
                         HttpResponse, 
                         JsonResponse)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .notify import NotifyMe


def feedback_message(request: HttpRequest) -> JsonResponse:
    message = FeedBackMessage.objects.create(name=request.POST.get("name"),
                            email=request.POST.get("email"),
                            phone=request.POST.get("phone"),
                            message=request.POST.get("message"))
    message.save()

    # send nofification
    notify = NotifyMe(name=request.POST.get("name"),
                      phone=request.POST.get("phone"),subject="Feedback/Issues",
                      message=request.POST.get("message"),date=message.date_sent)
    notify.notify_by_email()

    return render(request, 'htmx_message_templates/feedback_message.html', {"message":"Message dilivered"})


"""Customer issues"""
def customer_care(request: HttpRequest) -> JsonResponse:
    message = CustomerCare.objects.create(name=request.POST.get("name"),
                            email=request.POST.get("email"),
                            phone=request.POST.get("phone"),
                            problem=request.POST.get("message"))
    message.save()

    # send nofification
    notify = NotifyMe(name=request.POST.get("name"),
                      phone=request.POST.get("phone"),subject="Customer Care",
                      message=request.POST.get("message"),date=message.date_sent)
    notify.notify_by_email()

    return render(request, 'htmx_message_templates/feedback_message.html', {"message":"Issue Reported"})


@login_required_htmx
@require_http_methods(['POST'])
def like_hostel(request: HttpRequest):
    hostel = HostelProfile.objects.get(hostel_id=request.POST.get('hostel_id'))
    if HostelLike.objects.filter(user=request.user, hostel=hostel).exists():
        hostel.no_of_likes-=1
        hostel.save()
    else:
        liked = HostelLike.objects.create(user=request.user, hostel=hostel)
        liked.save()
        hostel.no_of_likes+=1
        hostel.save() 


