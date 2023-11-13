# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# from campus_app.models import CampusProfile
# from .models import CustomUser


# @api_view(['POST'])
# def signup_api(request):
#     if request.method == 'POST':
#         if CampusProfile.objects.filter(campus_code=str(request.data.get('campus')).upper().strip()).exists():
#             ##Getting campus model for quering hostels related to it
#             get_campus=CampusProfile.objects.get(campus_code=str(request.data.get('campus')).upper().strip())

#             ##checks if password if equal
#             if request.data.get('password') == request.data.get('confirm_password'):
                    
#                     #existance of phone number 
#                     if CustomUser.objects.filter(phone=request.data.get('phone')).exists():
#                         messages.info(request, 'Phone Number already registered')

                    
#                     elif CustomUser.objects.filter(email=request.data.get('email')).exists():
#                         return Response({'message':'Eamil has already been registered'})
                    
#                     elif CustomUser.objects.filter(student_id = request.data.get('student_id')).exists():
#                         return Response({'message':messages.info(request, 'Stundent has already been registered')

#                     else:
#                         """Creation of user model with details submitted"""
#                         create_user = CustomUser.objects.create_user(first_name=request.data.get('first_name'), 
#                             last_name=request.data.get('last_name'), middle_name=request.data.get('middle_name') ,
#                             email=request.data.get('email'), campus=get_campus, 
#                             username=f"{request.data.get('first_name')}_{request.data.get('middle_name')} {request.data.get('last_name')}",

#                             password=request.data.get('password'), phone=request.data.get('phone'), 
#                             student_id=request.data.get('student_id'),)
#                         create_user.save()

#                         """Log user in after user have been registed"""
#                         login_user = auth.authenticate(email=request.data.get('email'), password=request.data.get('password'))
#                         auth.login(request, login_user)

#                         send_mail(from_email=settings.EMAIL_HOST_USER, 
#                         recipient_list=[request.user.email], 
#                         subject=f'Congrats {request.user.username}. Your Sign Up seccessfull', 
#                         message=render_to_string('emails/signup_congrat.html',{'user':request.user}),
#                         fail_silently=True)

#                         return Response({'message':status=) 

#             else:
#                 return Response(messages.error(request, 'Password is not matching'))
#                 return redirect('accounts:signup')
            
#         else:
#             messages.info(request, 'BookUp is not yet registered on your campus')
        
#     # return render(request, 'forms/signup.html',)  