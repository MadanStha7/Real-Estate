from django.core.exceptions import PermissionDenied
from functools import wraps
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required


def user_is_authenticated(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrap


def user_is_superuser(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrap


def user_is_staff(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrap


def user_is_active(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if (
            request.user.is_active and request.user.has_perm
        ) or request.user.is_admin:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrap


def user_is_active(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_active:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrap


def user_is_agent(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='Agent').exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrap


def user_is_buyer_seller(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='BuyerOrSeller').exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrap


def user_is_staff(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='Staff').exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrap





