from django.shortcuts import render
from .models import FeedBackMessage, CustomerCare
from django.http import (HttpRequest, 
                         HttpResponse, 
                         JsonResponse)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .notify import NotifyMe


@api_view(http_method_names=['POST'])
def feedback_message(request: HttpRequest) -> JsonResponse:
    message = FeedBackMessage.objects.create(name=request.data.get("name"),
                            email=request.data.get("email"),
                            phone=request.data.get("phone"),
                            message=request.data.get("message"))
    message.save()

    # send nofification
    notify = NotifyMe(name=request.data.get("name"),
                      phone=request.data.get("phone"),subject="Feedback/Issues",
                      message=request.data.get("message"),date=message.date_sent)
    notify.notify_by_email()

    return Response({"message":"Message dilivered"})


"""Customer issues"""
@api_view(http_method_names=['POST'])
def customer_care(request: HttpRequest) -> JsonResponse:
    message = CustomerCare.objects.create(name=request.data.get("name"),
                            email=request.data.get("email"),
                            phone=request.data.get("phone"),
                            problem=request.data.get("message"))
    message.save()

    # send nofification
    notify = NotifyMe(name=request.data.get("name"),
                      phone=request.data.get("phone"),subject="Customer Care",
                      message=request.data.get("message"),date=message.date_sent)
    notify.notify_by_email()

    return Response({"message":"Message dilivered"})