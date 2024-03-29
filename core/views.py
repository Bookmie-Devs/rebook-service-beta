"""Custom Imports"""
from typing import Any
from accounts.models import Student
from accounts.task import send_email_task, send_sms_task

from config.sms import send_sms_message
from .models import Booking
from .models import Tenant
from .filters import HostelFilter
from rooms_app.models import RoomProfile
from campus_app.models import CampusProfile
from hostel_app.models import HostelProfile
from reviews_app.models import RecomendationFeedBacks, FAQ
from rest_framework.decorators import api_view

"""Built in Packages"""
from django.shortcuts import render
from django.views import generic
from django.http import (HttpRequest, 
                        HttpResponse, 
                        HttpResponseRedirect, 
                        JsonResponse)
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.timezone import timedelta
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
import random
from campus_app.models import CampusProfile
from django.views.decorators.cache import cache_page
from django.conf import settings

@require_http_methods(['GET'])
# @cache_page(settings.BOOKMIE_CACHING_TIMEOUT * 3)
def index(request):
    campuses = CampusProfile.objects.all()
    # random a list of hostels to display
    # campuses = random.sample(population=list(campuses), k=len(list(campuses)))
    feedbacks = RecomendationFeedBacks.objects.all()
    context = {
    'campuses':campuses,
    'user':request.user, 
    'feedbacks':feedbacks,
    'faqs': FAQ.objects.all(),
    }
    return render(request, 'index.html', context)


class HostelListView(generic.ListView):
    def get(self, request: HttpRequest, campus_param_id:str ,*args: Any, **kwargs: Any) -> HttpResponse:
        """Get hostel that are related to particular campus and display it
        to the client"""
        campus = CampusProfile.objects.get(campus_param_id=campus_param_id)
        campus_hostels = HostelProfile.objects.filter(campus=campus, verified=True)
        
        #context for the pages
        context={'hostels':campus_hostels, 'campus':campus,'user':request.user}

        """if user search for hostel"""
        if request.GET:
            search_data = request.GET['search_data']            
            campus = CampusProfile.objects.get(campus_param_id=campus_param_id)
            #query of search 
            query = HostelProfile.objects.filter(
            Q(verified=True) & 
            Q(campus=campus) & 
            (
            Q(hostel_name__icontains=search_data) |
            Q(location__icontains=search_data)
            )
            )
            #context containg search query page
            context['hostels']=query
            return render(request, 'htmx_templates/hostel_search_result.html', context)
        
        return render(request, 'campus_hostels.html', context)
    

# IN DEVELOPMENT 
@login_required()
def update_vcode(request):
    """update tenant year of staying"""

    # check if tenant is still active
    student = Student.objects.get(user=request.user)
    try:
        tenant = Tenant.objects.get(student=student)
        if tenant.is_active():
            messages.error(request,"Tenant V-code hasn't expired yet")
            return redirect("accounts:booking-and-payments")
        
        else:
            tenant.delete_if_expired()
            booked_room = RoomProfile.objects.get(room_id=request.POST.get('room_id')) 
            booking=Booking.objects.create(
            room=booked_room, 
            user=request.user, 
            room_number=booked_room.room_no,
            hostel=booked_room.hostel, 
            student_id=request.user.student_id, 
            status='Booked',
            end_time=(timezone.now() + timedelta(seconds=40)),
            campus=booked_room.campus,
            #for payment app to what type of booking
            is_updating_vcode=True)
            booking.save()
            messages.error(request,"Please proceed to payment")
            return redirect("accounts:booking-and-payments")
            
    except Tenant.DoesNotExist:
        messages.error(request,"Not a Tenant at current hostel")
        return redirect("accounts:booking-and-payments")
    
    
    
# Tenant.objects.filter(is)
@login_required()
def delete_booking(request):
    student = Student.objects.get(user=request.user)
    try:
        booking = Booking.objects.get(student=student)
        booking.delete()
        
        #  delete any payment history id any
        from payments_app.models import PaymentHistory

        if PaymentHistory.objects.filter(student=student, successful=False).exists():
            PaymentHistory.objects.filter(student=student, successful=False).delete()
            pass
        else:
            pass
        return redirect('accounts:booking-and-payments')
    
    except Booking.DoesNotExist:
        messages.info(request, 'No booking exits for this user')
        return redirect('accounts:booking-and-payments')

@login_required()
def success_message(request):

    return render(request, 'successful.html')


class AboutView(TemplateView):

    template_name = 'home/about.html'


def free_booking(request, room_id):
    acquired_room = RoomProfile.objects.get(room_id=room_id)
    student = Student.objects.get(user=request.user)
    tenant = Tenant.objects.create(
    payed=True, 
    student=student, 
    room=acquired_room,                                    
    hostel=acquired_room.hostel, 
    completed_payment=True)
    tenant.save()
    count_members: int = Tenant.objects.filter(
    room=acquired_room, 
    end_date__gt=acquired_room.campus.end_of_acadamic_year).count()

    # SET ROOM TO FULL IF CAPACITY HAS BEEN FIELED OR REDUCE BED SPACE LEFT
    acquired_room.reduce_bed_spaces(count_members=count_members)
    # change the room gender if the room is open and the the tenant is the first person
    acquired_room.change_room_gender(members=count_members,user_gender=request.user.gender)

    current_domain = request.META.get('HTTP_X_FORWARDED_HOST', request.META['HTTP_HOST'])
    # send sms
    # msg = render_to_string('emails/tenant_sms.html',{"user":request.user,"tenant":tenant,"amount":payment.amount,"domain":current_domain})
    # send_sms_message(user_contact=request.user.phone, msg=msg)
    # send sms to manager
    manager_msg = render_to_string(
    'emails/hostel_manager_msg.html',
    {'manager':tenant.hostel.hostel_manager,
    'tenant':tenant})
    send_sms_message(user_contact=tenant.hostel.hostel_manager.phone,msg=manager_msg)

    # send emails
    # subject = f'Confirmation: Your Room Booking is Complete!'
    # send_email_task(from_email=settings.EMAIL_HOST_USER, fail_silently=True,
    # recipient_list=[request.user.email], subject=subject, 
    # message=render_to_string('emails/tenant_email.html',{"user":request.user,"tenant":tenant,"amount":payment.amount,"domain":current_domain})),
    return redirect('core:success')


def site_map(request):
    return render(request, 'sitemap.xml', content_type="application/xhtml+xml")