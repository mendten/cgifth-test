from django.shortcuts import HttpResponseRedirect, render#type: ignore
from django.urls import reverse #type: ignore

from points.models import User
from points.wrappers import admin_only #type: ignore


@admin_only
def add_staff(request):
    program = request.user.program
    if request.method == 'GET':
        return render(request, 'points/add_staff.html')
    else:
        position = request.POST['position']
        names = request.POST['names'].splitlines()
        for name in names:
            # remove whitespace from the beginning and end of the name
            name = name.strip()
            first, last = name.rsplit(' ', 1)
            username = first[0] + last
            user = User(
                program=program,
                username=username, 
                first_name=first.title(), 
                last_name=last.title(), 
                position=position
            )
            user.set_password(username.lower())
            user.save()
        return HttpResponseRedirect(reverse('index'))
