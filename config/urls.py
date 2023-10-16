from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.conf.urls import handler404, handler500
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_view

# error handlers
handler404 = TemplateView.as_view(template_name='error/404.html')
handler500 = TemplateView.as_view(template_name='error/500.html')

app_name='main'
urlpatterns = [
    # url(r'^docs/', include('rest_framework_swagger.urls')), 
    path('admin/', admin.site.urls),
    path('', include('core.urls'), name='core_urls'),
    path('hostel/', include('hostel_app.urls'), name='hostel_urls'),
    path('room/', include('rooms_app.urls'), name= 'room_urls'),
    path('accounts/', include('accounts.urls'), name='accounts_urls'),
    path('payments/', include('payments_app.urls'), name='payment_urls'),
    path('reviews/', include('reviews_app.urls'), name='review_urls'),
    path('map/', include('maps_app.urls'), name='map'),
    path('management/', include('management_app.urls'), name='management'),

    #Account related urls for reseting passwords
    path('change-password/done/', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('change-password/', auth_view.PasswordChangeView.as_view(), name='change_password'),
    path('reset-password/', auth_view.PasswordResetView.as_view(template_name='forms/password_reset_email_form.html'), name='reset_password'),
    path('password-reset-done/', auth_view.PasswordResetDoneView.as_view(template_name='forms/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='forms/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='forms/password_reset_complete.html'), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

        