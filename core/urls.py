from django.urls import path
from django.urls import include
from . import views
from . import api_views
from . import booking


app_name ='core'

urlpatterns =[
    path('', views.index, name='index'),

    #generate campus related hostels to user base campus
    path('campus-hostels/<str:campus_code>/', views.HostelListView.as_view(), name='hostels'),

    path('booking/', booking.book_room, name='booking'),
    path('update-v-code/',views.update_vcode, name='update-v-code'),
    path('delete-booking/', views.delete_booking, name='delete-booking'),
    path('verification/success/', views.success_message, name="success"),

    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('news-letter/', views.news_letter, name="news-letter"),

    # APIS
    path('api/hostels/<str:campus_code>/', api_views.HostelListView.as_view(), name='api_hostels'),
]