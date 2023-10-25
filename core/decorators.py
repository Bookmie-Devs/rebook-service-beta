from django.shortcuts import redirect
from django.contrib.auth.models import User
User.get_group_permissions
from django.contrib import messages

# print(type(User.get_group_permissions))

def authenticated_or_not(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
             messages.info(request=request,
                           message="You are already login", 
                           fail_silently=True)
             return redirect('accounts:booking-and-payments')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function


def check_user(view_function, allowed_user):
    def wrapper_function(request, *args, **kwargs):
        get_group = request.user.get_group_permissions[0]
        if get_group==allowed_user[0]:
            pass

