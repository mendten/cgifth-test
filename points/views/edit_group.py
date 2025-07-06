from django.shortcuts import HttpResponseRedirect, render #type: ignore
from django.urls import reverse #type: ignore
from points.models import Group, Camper
from points.wrappers import admin_only #type: ignore


@admin_only
def edit_group(request):
    program = request.user.program
    if request.method == 'GET':
        bunks = Group.objects.filter(group_type='bunk', program=program).order_by('number')
        classes = Group.objects.filter(group_type='learning_class', program=program).order_by('number')
        free_campers_bunk = Camper.objects.filter(new_bunk__isnull=True).order_by('last_name')
        free_campers_lc = Camper.objects.filter(new_class__isnull=True).order_by('last_name')
        return render(request, 'points/edit_group.html', {
            'bunks': bunks,
            'classes': classes,
            'free_campers_bunk': free_campers_bunk,
            'free_campers_lc': free_campers_lc,
        })
    else:
        if request.POST['action'] == 'remove':
            # get list of campers who were checked off in page
            campers = request.POST.getlist('camper')
            for camper in campers:
                camper = Camper.objects.get(pk=camper)
                if 'bunk' in request.POST:
                    camper.new_bunk = None
                else:
                    camper.new_class = None
                camper.save()
        elif request.POST['action'] == 'add':
            # get list of campers who were checked off in page
            campers = request.POST.getlist('camper')
            for camper in campers:
                camper = Camper.objects.get(pk=camper)
                if request.POST['group'] == 'bunk':
                    group = Group.objects.get(group_type='bunk', number=request.POST['group-id'].rsplit('-', 1)[1])
                    camper.new_bunk = group
                else:
                    lc = Group.objects.get(group_type='learning_class', number=request.POST['group-id'].rsplit('-', 1)[1])
                    camper.new_class = lc
                camper.save()
        return HttpResponseRedirect(reverse('edit_group'))
