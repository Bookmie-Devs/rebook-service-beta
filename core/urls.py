from django.urls import path
from django.urls import include
from . import views

app_name ='core'

urlpatterns =[
    path('', views.index, name='home'),
    path('booking/<str:room_id>/', views.book_room, name='book'),
    path('Campus_Hostels/<str:campus_code>/', views.CampusHostels, name='Base'),
    path('search/',views.search, name='search'),
    path('booking-verification/<str:booking_id>/', views.booking_success, name='booking_ver')
]