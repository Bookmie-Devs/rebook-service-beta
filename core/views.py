"""Custom Imports"""
from typing import Any
from .models import Booking
from .models import Tenant
from .filters import HostelFilter
from rooms_app.models import RoomProfile
from campus_app.models import CampusProfile
from hostel_app.models import HostelProfile
from reviews_app.models import RecomendationFeedBacks
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
@cache_page(settings.BOOKMIE_CACHING_TIMEOUT * 3)
def index(request):
    campuses = CampusProfile.objects.all()
    # random a list of hostels to display
    # campuses = random.sample(population=list(campuses), k=len(list(campuses)))

    feedbacks = RecomendationFeedBacks.objects.all()
    return render(request, 'index.html', {'campuses':campuses,'user':request.user, 'feedbacks':feedbacks})


class HostelListView(generic.ListView):
    def get(self, request: HttpRequest, campus_code:str ,*args: Any, **kwargs: Any) -> HttpResponse:
        """Get hostel that are related to particular campus and display it
        to the client"""
        campus = CampusProfile.objects.get(campus_code=campus_code)
        campus_hostels = HostelProfile.objects.filter(campus=campus, verified=True)
        
        #context for the pages
        context={'hostels':campus_hostels, 'campus':campus,'user':request.user}

        """if user search for hostel"""
        if request.GET:
            search_data = request.GET['search_data']            
            campus = CampusProfile.objects.get(campus_code=campus_code)
            #query of search 
            query = HostelProfile.objects.filter(Q(verified=True) & Q(campus=campus) & (Q(hostel_name__icontains=search_data) | Q(location__icontains=search_data)))
            #context containg search query page
            context['hostels']=query
            return render(request, 'htmx_templates/hostel_search_result.html', context)
        
        return render(request, 'campus_hostels.html', context)
    

# IN DEVELOPMENT 
def update_vcode(request):
    """update tenant year of staying"""

    # check if tenant is still active
    try:
        tenant = Tenant.objects.get(user=request.user)
        if tenant.is_active():
            messages.error(request,"Tenant V-code hasn't expired yet")
            return redirect("accounts:booking-and-payments")
        
        else:
            tenant.delete_if_expired()
            booked_room = RoomProfile.objects.get(room_id=request.POST.get('room_id')) 
            booking=Booking.objects.create(room=booked_room, user=request.user, 
                                      room_number=booked_room.room_no, hostel=booked_room.hostel, 
                                      student_id=request.user.student_id, status='Booked',
                                      end_time=(timezone.now() + timedelta(seconds=40)),
                                      campus=booked_room.campus)
            booking.save()
            messages.error(request,"Please proceed to payment")
            return redirect("accounts:booking-and-payments")
            
    except Tenant.DoesNotExist:
        messages.error(request,"Not a Tenant at current hostel")
        return redirect("accounts:booking-and-payments")
    
    
    
# Tenant.objects.filter(is)
@login_required()
def delete_booking(request):
    try:
        booking = Booking.objects.get(user=request.user)
        booking.delete()
        
        #  delete any payment history id any
        from payments_app.models import PaymentHistory

        if PaymentHistory.objects.filter(user=request.user).exists():
            PaymentHistory.objects.get(user=request.user).delete()
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

class ContactView(TemplateView):
    
    template_name = 'home/contact.html'


class AboutView(TemplateView):

    template_name = 'home/about.html'


@api_view(['POST'])
def news_letter(request: HttpRequest):
    from .models import NewsletterEmails
    news_letter = NewsletterEmails.objects.create(email=request.data.get('email'))
    news_letter.save()

    return JsonResponse({"message":"submitted"})



    