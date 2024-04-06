"""Custom imports"""
from .models import CustomUser
from .models import Student
from core.decorators import authenticated_or_not
from config.sms import send_sms_message
from campus_app.models import CampusProfile
from .models import Student
from core.models import Booking, Tenant
from core.phone import check_number
from .task import send_email_task

"""Built in packages"""
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib import auth
from django.template.loader import render_to_string

def render_message(request, message, tag):
    return render(request, 'htmx_message_templates/message.html', {'message': message, 'tag': tag})


def redirect_To_complete_profile(request, user):
    messages.success(request, 'Please confirm and complete profile.', extra_tags='success')
    response = HttpResponse()
    response['HX-Redirect'] = f'/accounts/complete-profile/{user.user_uuid}/'
    return response


def signup(request: HttpRequest):
    """ CustomUser signup View"""
    campuses = CampusProfile.objects.filter(available_on_campus=True).all()

    if request.method == 'POST':
        campus_code = request.POST.get('campus_code', '').upper().strip()
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        phone = request.POST.get('phone', '')
        student_id_number = request.POST.get('student_id_number', '')

        # Check if campus exists
        if CampusProfile.objects.filter(campus_code=campus_code, available_on_campus=True).exists():
            get_campus = CampusProfile.objects.get(campus_code=campus_code)

            # Check if passwords match
            if password != confirm_password:
                return render_message(request, 'Password is not matching', 'danger')

            try:
                validate_password(confirm_password)

                # Check if phone number is valid
                if check_number(phone) == 400:
                    return render_message(request, 'Phone number incorrect, please go back and check', 'danger')
                
                # Check if email exists
                elif CustomUser.objects.filter(email=email, is_active=True).exists():
                    return render_message(request, 'Email has already been registered', 'warning')

                elif CustomUser.objects.filter(email=email, is_active=False).exists():
                    user = CustomUser.objects.get(email=email, is_active=False)
                    return redirect_To_complete_profile(request, user)
                
                # Check if phone number exists
                elif CustomUser.objects.filter(phone=phone, is_active=True).exists():
                    return render_message(request, 'Phone Number has already been registered', 'info')

                elif CustomUser.objects.filter(phone=phone, is_active=False).exists():
                    user = CustomUser.objects.get(phone=phone, is_active=False)
                    return redirect_To_complete_profile(request, user)

                   # Check if student ID exists and is_active
                elif Student.objects.filter(student_id_number=student_id_number, user__is_active=True).exists():
                    return render_message(request, 'Account with student ID already exists (check ID)', 'danger')

                # Check if student ID exists
                elif Student.objects.filter(student_id_number=student_id_number, user__is_active=False).exists():
                    user = Student.objects.get(student_id_number=student_id_number, user__is_active=False).user
                    return redirect_To_complete_profile(request, user)
                
                # Create user and student
                new_user: CustomUser = CustomUser.objects.create_user(
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    middle_name=request.POST.get('middle_name'),
                    email=email,
                    is_student=True,
                    username=f"{request.POST.get('first_name')}_{request.POST.get('middle_name')} {request.POST.get('last_name')}",
                    password=password,
                    phone=check_number(phone),
                    gender=request.POST.get('gender', '').lower(),
                    is_active=False
                )
                new_user.save()

                student = Student.objects.create(user=new_user, student_id_number=student_id_number, campus=get_campus)
                student.save()
                return redirect_To_complete_profile(request, new_user)
            
            except ValidationError as e:
                error_message = e.messages[0] if e.messages else 'Invalid password'
                return render_message(request, error_message, 'warning')

        else:
            return render_message(request, 'Bookmie.com is not yet registered on your campus', 'info')

    return render(request, 'forms/signup.html', {'campuses': campuses})


def complete_profile(request: HttpRequest, user_uuid):
    campuses = CampusProfile.objects.filter(available_on_campus=True).all()
    student = Student.objects.get(user__user_uuid=user_uuid)
    if request.method == "POST":
        if student.user.is_active:
            messages.success(request, 'Account active, please login.', extra_tags='success')
            response = HttpResponse()
            response['HX-Redirect'] = f'/accounts/booking-and-payments'
        campus_code = request.POST.get('campus_code')
        campus = CampusProfile.objects.get(campus_code=campus_code)
        # Update user profile data based on form submission
        student.user.first_name = request.POST.get('first_name')
        student.user.email = request.POST.get('email')
        student.user.middle_name = request.POST.get('middle_name', '')
        student.user.last_name = request.POST.get('last_name')
        student.user.phone = request.POST.get('phone', '')
        student.campus = campus
        student.student_id_number = request.POST.get('student_id_number')
        # Repeat for other fields  return response
        student.user.save()

        # Send verification email
        send_verification_email(request=request, user=student.user)

        return render_message(request, 'Please check your email to activate your account.', 'info')
    context = {'user':student.user, 'campuses':campuses, 'student':student}
    return render(request, 'complete_profile.html',context)


@authenticated_or_not
def login(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        login_user = auth.authenticate(email=email, password=password)
        if login_user is not None:
            auth.login(request, login_user)
            # current_domain == get_current_site(request)
            # send user notice of login
            current_domain = request.META.get('HTTP_X_FORWARDED_HOST', request.META['HTTP_HOST'])
            msg = render_to_string("emails/login_email.html", {'user':request.user,'time':timezone.now(),'domain':current_domain})
            if request.user.is_hostel_worker or request.user.is_hostel_manager:
                # send_sms_task.delay(request.user.phone, msg)
                subject = 'Account Alert'
                send_email_task(subject, msg, settings.EMAIL_HOST_USER, [request.user.email])
                return redirect("management:portar-office")
            # send_sms_message
            """
            Send sms with celery
            """
            current_site = get_current_site(request)
            subject = 'Account Alert'
            send_email_task(subject, msg, settings.EMAIL_HOST_USER, [request.user.email])
            return redirect('accounts:booking-and-payments')
        else:
            messages.error(request, 'Credentials invalid', extra_tags="danger")
            return redirect('accounts:login')

    return render(request, 'forms/login.html')

@login_required()
def logout(request):
    auth.logout(request)
    return redirect('core:index')


@login_required()
def booking_and_payments(request: HttpRequest):
    user =request.user
    student = Student.objects.get(user=user)
    context = {'user':user, 'student':student, 'is_private_booking':False}
    if user.is_hostel_manager or user.is_hostel_worker:
        return redirect("management:portar-office")

    elif Booking.objects.filter(student=student).exists():
        booking = Booking.objects.get(student=student)
        tenant = False
        context.update({'tenant':tenant,'booking': booking,})
        return render(request, 'booking_and_payments.html', context)
    
    elif Tenant.objects.filter(student=student).exists():
        tenant = Tenant.objects.get(student=student)
        booking = False
        context.update({'tenant':tenant,'booking': booking,})
        return render(request, 'booking_and_payments.html', context)
    
    else:
        return render(request, 'booking_and_payments.html', context)

# EMAIL VERIFICATION
from .tokens import account_activation_token

def send_verification_email(request, user: CustomUser) -> None:
    from django.core.mail import EmailMessage
    from django.contrib.sites.shortcuts import get_current_site
    from django.template.loader import render_to_string
    from django.utils.http import urlsafe_base64_encode
    current_site = get_current_site(request)
    subject = 'Activate Your Bookmie Account'
    message = render_to_string('emails/email_verification_message.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(user.email.encode()),
        'token': account_activation_token.make_token(user),
    })  
    to_email = user.email
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, to=[to_email])
    email.content_subtype = "html"
    email.send(fail_silently=True)


def activate(request, uidb64, token):
    from django.utils.http import urlsafe_base64_decode
    from .models import CustomUser
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = CustomUser.objects.get(email=uid.decode('utf-8'))
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        # sms message for testing
        # will celery later to send sms
        msg = render_to_string('emails/signup_sms.html',{'user':request.user})
        send_sms_message(user_contact=request.user.phone, msg=msg)
        # # email msg with celery
        email_message = render_to_string('emails/signup_congrat.html',{'user':request.user})
        # send_email_task.delay(f'Welcome to Bookmie.com!, {request.user.username} Your signup was successful.', 
        #                 email_message, 
        #                 settings.EMAIL_HOST_USER, 
        #                 [request.user.email])
        # for testing
        send_email_task(f'Welcome to Bookmie.com!, {request.user.username} Your signup was successful.', 
                        email_message, 
                        settings.EMAIL_HOST_USER, 
                        [request.user.email])
        messages.success(request, 'Your account has been activated successfully.', extra_tags="info")
        return redirect('accounts:booking-and-payments')
    
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('accounts:login')
