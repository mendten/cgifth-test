from django.shortcuts import HttpResponseRedirect #type: ignore
from django.urls import reverse #type: ignore


def admin_only(func):
    """Decorator, checks if user associated with request is a league admin or ref"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.position != 'admin':
            return HttpResponseRedirect(reverse('index'))
        else:
            return func(request, *args, **kwargs)
    return wrapper