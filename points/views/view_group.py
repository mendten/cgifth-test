from django.shortcuts import render #type: ignore
from points.models import Group #type: ignore

from points.wrappers import admin_only #type: ignore


@admin_only
def view_group(request):
    program = request.user.program
    if request.method == 'GET':
        bunks = Group.objects.filter(group_type='bunk', program=program).order_by('number')
        classes = Group.objects.filter(group_type='learning_class', program=program).order_by('number')
        return render(request, 'points/view_group.html', {
            'bunks': bunks,
            'classes': classes,
        })
