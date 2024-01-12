from django.shortcuts import redirect
from django.contrib.auth.models import User
User.get_group_permissions
from django.contrib import messages

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.contrib.auth.decorators import login_required as django_login_required
from django.http import HttpResponse, HttpRequest
from functools import wraps
from functools import wraps
from django.shortcuts import resolve_url


def authenticated_or_not(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
             return redirect('accounts:booking-and-payments')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function


def check_user(view_function, allowed_user):
    def wrapper_function(request, *args, **kwargs):
        get_group = request.user.get_group_permissions[0]
        if get_group==allowed_user[0]:
            pass


def custom_login_required(function=None, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated and request.htmx:
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            return HttpResponse(status=204, headers={'HX-Redirect': resolved_login_url})
        return django_login_required(
            function=function,
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )(request, *args, **kwargs)
    return wrapper


def login_required_htmx(view_func=None, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            return HttpResponse(status=204, headers={'HX-Redirect': resolved_login_url})
    return _wrapped_view
