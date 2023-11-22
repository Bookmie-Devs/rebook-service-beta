from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import CampusProfile
from django.views.generic import ListView
# Create your views here.



class CampusListView(ListView):
    
    def get(self, request: HttpRequest, router_value:str, *args: Any, **kwargs: Any) -> HttpResponse:

        campuses = CampusProfile.objects.filter(available_on_campus=True).all()
        context = {
            "campuses" : campuses
        }
        context["campuses"] = campuses 
        if router_value == "hostel-router": 
            # check router value and route to appopraite tmeplate 
            return render(request, template_name='home/hostel_redirect.html', context=context)
            
        elif router_value=='room-router':
            # check router value and route to appopraite tmeplate 
            return render(request, template_name='home/room_redirect.html',context=context)

