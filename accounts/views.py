"""Custom imports"""
from .models import CustomUser
from core.decorators import authenticated_or_not
from config.sms import send_sms_message
from campus_app.models import CampusProfile
from core.models import Booking, Tenant

"""Built in packages"""
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from config.phone import check_number

require_http_methods(["POST"])
def signup(request):
    """ CustomUser signup View"""

    if request.method == 'POST':
        if CampusProfile.objects.filter(campus_code=str(request.POST.get('campus')).upper().strip()).exists():
            ##Getting campus model for quering hostels related to it
            get_campus=CampusProfile.objects.get(campus_code=str(request.POST.get('campus')).upper().strip())

            ##checks if password if equal
            if request.POST.get('password') == request.POST.get('confirm_password'):
                try:
                    validate_password(request.POST.get('confirm_password'))

                    # checking if number is valid
                    if check_number(request.POST.get('phone')) == "number-error":
                        
                        message ={'message':'Phone number is not in the correct format or incorrect'}
                        return render(request,'htmx_message_templates/message.html', message)
                    
                    #existance of phone number 
                    elif CustomUser.objects.filter(phone=request.POST.get('phone')).exists():
                        # htmx message for signup
                        message ={'message':'Phone Number has already been registered'}
                        return render(request,'htmx_message_templates/message.html', message)
                    
                    elif CustomUser.objects.filter(email=request.POST.get('email')).exists():
                        # htmx message for signup
                        message ={'message':'Eamil has already been registered'}
                        return render(request,'htmx_message_templates/message.html', message)

                    
                    elif CustomUser.objects.filter(student_id = request.POST.get('student_id')).exists():
                        # messages.info(request, 'Stundent has already been registered')
                        # return redirect('accounts:signup')
                        # htmx message for signup
                        message ={'message':'Account with studnet ID already exists(check ID)'}
                        return render(request,'htmx_message_templates/message.html', message)
                        

                    else:
                        """Creation of user model with details submitted"""
                        create_user = CustomUser.objects.create_user(first_name=request.POST.get('first_name'), 
                            last_name=request.POST.get('last_name'), middle_name=request.POST.get('middle_name') ,
                            email=request.POST.get('email'), campus=get_campus, 
                            username=f"{request.POST.get('first_name')}_{request.POST.get('middle_name')} {request.POST.get('last_name')}",

                            password=request.POST.get('password'), phone=check_number(request.POST.get('phone')), 
                            student_id=request.POST.get('student_id'),)
                        create_user.save()

                        """Log user in after user have been registed"""
                        login_user = auth.authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
                        auth.login(request, login_user)
                        # sms message
                        msg = render_to_string('emails/signup_congrat.html',{'user':request.user})
                        send_sms_message(user_contact=request.user.phone, msg=msg)
                        # email msg
                        send_mail(from_email=settings.EMAIL_HOST_USER, 
                        recipient_list=[request.user.email], 
                        subject=f'Welcome to Bookmie.com!, {request.user.username} Your signup was successful.', 
                        message=render_to_string('emails/signup_congrat.html',{'user':request.user}),
                        fail_silently=True)

                        response = HttpResponse()
                        response['HX-Redirect'] = '/accounts/booking-and-payments/'
                        return response
                    
                    
                except ValidationError as e:
                    for err in e:
                        message ={'message':f'{err}'}
                        return render(request,'htmx_message_templates/message.html', message)

            else:
                # htmx message for signup
                message ={'message':'Password is not matching'}
                return render(request,'htmx_message_templates/message.html', message)

            
        else:
            # htmx message for signup
            message ={'message':'BookUp is not yet registered on your campus'}
            return render(request,'htmx_message_templates/message.html', message)
        
        
    return render(request, 'forms/signup.html',)  




@authenticated_or_not
def login(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        login_user = auth.authenticate(email=email, password=password)
        if login_user is not None:
            auth.login(request, login_user)
            # send_sms_message
            current_domain = request.META.get('HTTP_X_FORWARDED_HOST', request.META['HTTP_HOST'])
            msg = render_to_string("emails/login_sms.html", {'user':request.user,'time':timezone.now(),
                                                             'domain':current_domain})
            send_sms_message(user_contact=request.user.phone ,msg=msg)

            return redirect('accounts:booking-and-payments')
        else:
            messages.error(request, 'Credentials invalid')
            return redirect('accounts:login')

    return render(request, 'forms/login.html')

@login_required()
def logout(request):
    auth.logout(request)
    return redirect('core:index')


@login_required()
def booking_and_payments(request):
    get_user = CustomUser.objects.get(id=request.user.id)

    if Booking.objects.filter(user=request.user).exists():
        booking = Booking.objects.get(user=request.user)
        tenant = False
        context = {'user':get_user, 
                   'tenant':tenant,
                   'booking': booking,}
        return render(request, 'booking_and_payments.html',context=context)

    elif Tenant.objects.filter(user=request.user).exists():
        tenant = Tenant.objects.get(user=request.user)
        booking = False
        context = {'user':get_user, 
                   'booking': booking,
                   'tenant':tenant}
        return render(request, 'booking_and_payments.html',context=context)
    
    else:
        return render(request, 'booking_and_payments.html')