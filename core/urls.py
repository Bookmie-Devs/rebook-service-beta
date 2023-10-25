from django.urls import path
from django.urls import include
from . import views
from django.contrib.auth.decorators import login_required

app_name ='core'

urlpatterns =[
    path('', views.index, name='index'),

    #generate campus related hostels to user base campus
    path('hostels/<str:campus_code>', views.HostelListView.as_view(), name='hostels'),

    path('booking/', views.book_room, name='booking'),
    path('update-v-code/',views.update_vcode, name='update-v-code'),
    path('delete-booking/', views.delete_booking, name='delete-booking'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('verification/success/', views.success_message, name="success")
]