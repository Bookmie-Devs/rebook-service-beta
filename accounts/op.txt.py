
# require_http_methods(["POST"])
# def signup(request: HttpRequest):
#     """ CustomUser signup View"""
#     campuses = CampusProfile.objects.filter(available_on_campus=True).all()
#     if request.method == 'POST':
#         campus_code = str(request.POST.get('campus_code')).upper().strip()
#         if CampusProfile.objects.filter(campus_code=campus_code,  available_on_campus=True).exists():
#             ##Getting campus model for quering hostels related to it
#             get_campus=CampusProfile.objects.get(campus_code=campus_code)
#             email =request.POST.get('email').lower()
#             ##checks if password if equal
#             if request.POST.get('password') == request.POST.get('confirm_password'):
#                 try:
#                     validate_password(request.POST.get('confirm_password'))

#                     # checking if number is valid
#                     if check_number(request.POST.get('phone')) == 400:
#                         message ={'message':'Phone number incorrect, please go back and check','tag':'danger'}
#                         return render(request,'htmx_message_templates/message.html', message)
                    
#                     #existance of phone number 
#                     elif CustomUser.objects.filter(phone=request.POST.get('ph   one')).exists():
#                         # htmx message for signup
#                         message ={'message':'Phone Number has already been registered','tag':'info'}
#                         return render(request,'htmx_message_templates/message.html', message)
                    
#                     elif CustomUser.objects.filter(email=email).exists():
#                         # htmx message for signup
#                         message ={'message':'Email has already been registered','tag':'warning'}
#                         return render(request,'htmx_message_templates/message.html', message)

#                     elif Student.objects.filter(student_id_number = request.POST.get('student_id_number')).exists():
#                         # messages.info(request, 'Stundent has already been registered')
#                         # return redirect('accounts:signup')
#                         # htmx message for signup
#                         message ={'message':'Account with studnet ID already exists(check ID)','tag':'danger'}
#                         return render(request,'htmx_message_templates/message.html', message)
                        
#                     else:
#                         """Creation of user model with details submitted"""
#                         new_user = CustomUser.objects.create_user(first_name=request.POST.get('first_name'), 
#                             last_name=request.POST.get('last_name'), middle_name=request.POST.get('middle_name') ,
#                             email=email, is_student=True,
#                             username=f"{request.POST.get('first_name')}_{request.POST.get('middle_name')} {request.POST.get('last_name')}",
#                             password=request.POST.get('password'), phone=check_number(request.POST.get('phone')), 
#                             gender=request.POST.get('gender').lower() ,is_active=False)
#                         new_user.save()

#                         student = Student.objects.create(user=new_user, student_id_number=request.POST.get('student_id_number'), campus=get_campus,)
#                         student.save()
                          
#                         # Send verification email
#                         send_verification_email(request=request, user=new_user)
                        
#                         messages.success(request, 'Please check your email to complete the registration.', extra_tags='success')
#                         response = HttpResponse()
#                         response['HX-Redirect'] = '/accounts/login/'
#                         return response
                    
#                 except ValidationError as e:
#                     for err in e:
#                         message ={'message':f'{err}','tag':'warning'}
#                         return render(request,'htmx_message_templates/message.html', message)

#             else:
#                 # htmx message for signup
#                 message ={'message':'Password is not matching','tag':'danger'}
#                 return render(request,'htmx_message_templates/message.html', message)

            
#         else:
#             # htmx message for signup
#             message ={'message':'Bookmie.com is not yet registered on your campus','tag':'info'}
#             return render(request,'htmx_message_templates/message.html', message)
        
        
#     return render(request, 'forms/signup.html', {'campuses':campuses})  












from django.shortcuts import render, redirect
from .models import TempUserData, UserData

def edit_details(request):
    if request.method == 'POST':
        # Handle form submission
        # Check if the user has verified their account
        if request.user.is_verified:
            # Update user data directly in the database
            UserData.objects.filter(user=request.user).update(**request.POST)
        else:
            # Store submitted data temporarily
            temp_data, created = TempUserData.objects.get_or_create(user=request.user)
            temp_data.data = request.POST
            temp_data.save()
        return redirect('profile')  # Redirect to user profile page
    else:
        # Display edit form with pre-filled data
        if request.user.is_verified:
            # Retrieve user data from the database
            user_data = UserData.objects.get(user=request.user)
            form_data = user_data.to_dict()
        else:
            # Retrieve temporarily stored data
            temp_data, created = TempUserData.objects.get_or_create(user=request.user)
            form_data = temp_data.data if temp_data else {}
        return render(request, 'edit_details.html', {'form_data': form_data})
