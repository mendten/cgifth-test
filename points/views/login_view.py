from django.shortcuts import HttpResponseRedirect, render #type: ignore
from django.contrib.auth import authenticate, login #type: ignore
from django.urls import reverse #type: ignore

from points.models import User


def login_view(request):
    if request.method == 'GET':
        return render(request, 'points/login.html')
    else:
        username = request.POST['username'].lower()
        for user in User.objects.all():
            if username == user.username.lower():
                username = user.username
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'points/login.html', {'message': 'Invalid username and/or password'})
