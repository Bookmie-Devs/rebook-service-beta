from django.shortcuts import redirect
from django.contrib.auth.models import User
User.get_group_permissions

# print(type(User.get_group_permissions))

def if_user_is_login(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
             return redirect('core:hostels')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function


def check_user(view_function, allowed_user):
    def wrapper_function(request, *args, **kwargs):
        get_group = request.user.get_group_permissions[0]
        if get_group==allowed_user[0]:
            pass

