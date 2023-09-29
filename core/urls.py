from django.urls import path
from django.urls import include
from . import views

app_name ='core'

urlpatterns =[
    path('', views.index, name='index'),

    #generate campus related hostels to user base campus
    path('hostels/', views.hostels, name='hostels'),

    path('booking/<str:room_id>/', views.book_room, name='book'),
    path('search/',views.search, name='search'),
]