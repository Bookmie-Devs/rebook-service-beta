from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from campus_app.models import CampusProfile
from django.contrib import messages
from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from .models import CustomUser
from django.template.loader import render_to_string
#user profile


def signup(request):
    """ CustomUser signup View"""

    if request.method == 'POST':
        try:
            print(request.POST.get('campus').upper())
            ##Getting campus model for quering hostels related to it
            get_campus=CampusProfile.objects.get(campus_code=request.POST.get('campus').upper())

            ##checks if password if equal
            if request.POST.get('password') == request.POST.get('confirm_password'):
                ##checks if password if long enough
                if len( request.POST.get('password')) < 2:
                    messages.error(request, 'Password is too short')
                    return redirect('Core:signup')
                #existance of phone number 
                elif CustomUser.objects.filter(phone=request.POST.get('phone')).exists():
                    messages.info(request, 'Phone Number already registered')
                    return redirect('Core:signup')
                
                elif CustomUser.objects.filter(email=request.POST.get('email')).exists():
                    messages.info(request, 'Eamil has already been registered')
                    return redirect('Core:signup')
                
                elif CustomUser.objects.filter(student_id = request.POST.get('student_id')).exists():
                    messages.info(request, 'Stundent has already been registered')
                    return redirect('Core:signup')

                else:
                    """Creation of user model with details submitted"""
                    create_user = CustomUser.objects.create_user(first_name=request.POST.get('first_name'), 
                        last_name=request.POST.get('last_name'), middle_name=request.POST.get('middle_name') ,
                        email=request.POST.get('email'), campus=get_campus, 
                        username=f"{request.POST.get('first_name')}_{request.POST.get('middle_name')} {request.POST.get('last_name')}",

                        password=request.POST.get('password'), phone=request.POST.get('phone'), 
                        student_id=request.POST.get('student_id'),).save()

                    """Log user in after user have been registed"""
                    login_user = auth.authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
                    auth.login(request, login_user)

                    send_mail(from_email=settings.EMAIL_HOST_USER, 
                    recipient_list=[request.user.email], 
                    subject=f'Congrats {request.user.username}. Your Sign Up seccessfull', 
                    message=render_to_string('TextTemplates/signup_congrat.html',{'user':request.user}),
                    fail_silently=True)
                    return redirect('core:home') 
            else:
                messages.error(request, 'Password is not matching')
                return redirect('Core:signup')
            
        except CampusProfile.DoesNotExist:
            messages.info(request, 'BookUp is not yet registered on your campus')
            return redirect('Core:signup')
        
    return render(request, 'forms/signup.html')  

# @if_user_is_login
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        student_id = request.POST.get('student_id')
        password = request.POST['password']
        if CustomUser.objects.filter(student_id=student_id).exists():
            login_user = auth.authenticate(email=email, password=password)
            if login_user is not None:
                auth.login(request, login_user)
                return redirect('Core:Base', kwargs={"campus_code":request.user.campus.campus_code})
            else:
                messages.error(request, 'Credentials invalid')
                return redirect('Core:login')
        else:
            messages.error(request, 'Invalid student ID')
            return redirect('accounts:login')
    return render(request, 'forms/login.html')

@login_required(login_url='Core:login')
def logout(request):
    auth.logout(request)
    return redirect('accounts:login')


def profile(request):
    get_user = CustomUser.objects.get(id=request.user.id)
    context={'user':get_user,'user_profile':''}
    return render(request, 'home/profile.html', context)

