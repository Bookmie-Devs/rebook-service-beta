from django.urls import path
from django.urls import include
from . import views

app_name ='core'

urlpatterns =[
    path('', views.index, name='index'),

    #generate campus related hostels to user base campus
    path('hostels/', views.hostels, name='hostels'),

    path('booking/', views.book_room, name='booking'),
    path('delete-booking/', views.delete_booking, name='delete-booking'),

    path('search/',views.search, name='search'),
]