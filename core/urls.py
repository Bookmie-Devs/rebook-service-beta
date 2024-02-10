from django.urls import path
from django.urls import include
from django.views.decorators.cache import cache_page
from django.conf import settings
from . import views
from . import api_views
from . import booking

app_name ='core'

time = settings.BOOKMIE_CACHING_TIMEOUT

urlpatterns =[
    path('', views.index, name='index'),

    #generate campus related hostels to user base campus
    path('campus-hostels/<str:campus_id>/',(cache_page(time))(views.HostelListView.as_view()), name='hostels'),

    path('booking/', booking.book_room, name='booking'),
    path('update-v-code/',views.update_vcode, name='update-v-code'),
    path('delete-booking/', views.delete_booking, name='delete-booking'),
    path('verification/success/', views.success_message, name="success"),

    path('about/', (cache_page(time*5))(views.AboutView.as_view()), name='about'),

    # APIS
    path('api/hostels/<str:campus_code>/', api_views.HostelListView.as_view(), name='api_hostels'),
]