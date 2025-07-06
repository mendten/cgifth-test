from django.shortcuts import redirect #type: ignore
from django.contrib.auth import logout #type: ignore
from django.contrib.auth.decorators import login_required #type: ignore
from django.urls import reverse #type: ignore


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))