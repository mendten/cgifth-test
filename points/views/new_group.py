from django.shortcuts import HttpResponseRedirect, render #type: ignore
from django.urls import reverse #type: ignore

from points.models import User, Group, Camper #type: ignore
from points.wrappers import admin_only #type: ignore


@admin_only
def new_group(request):
    program = request.user.program
    if request.method == 'GET':
        campers = Camper.objects.filter(new_class__isnull=True, program=program).order_by('last_name')
        counselors = User.objects.filter(position='counselor', program=program)
        lts = User.objects.filter(position='teacher')
        return render(request, 'points/new_group.html', {
            'campers': campers,
            'counselors': counselors,
            'lts': lts
            })
    else:
        if request.POST['group-type'] != 'campers-only':
            group = Group(program=program, name=request.POST['group-name'], number=request.POST['group-num'])
            group.save()
        if request.POST['group-type'] == 'bunk':
            group.group_type = 'bunk'
            counselor1 = User.objects.get(pk=request.POST['counselor-1'])
            group.staff.add(counselor1)
            if request.POST['counselor-2'] != 'none':
                counselor2 = User.objects.get(pk=request.POST['counselor-2'])
                group.staff.add(counselor2)
            group.save()
            first = request.POST.getlist('first-name')
            last = request.POST.getlist('last-name')
            father = request.POST.getlist('father-email')
            mother = request.POST.getlist('mother-email')
            for i in range(len(first)):
                if first[i] != '':
                    camper = Camper(program=program,
                                    first_name=first[i].title(), 
                                    last_name=last[i].title(), 
                                    new_bunk=group, 
                                    father_email=father[i], 
                                    mother_email=mother[i])
                    camper.save()
        elif request.POST['group-type'] == 'class':
            group.group_type = 'learning_class'
            lt = User.objects.get(pk=request.POST['lt'])
            group.staff.add(lt)
            group.save()
            campers = request.POST.getlist('camper-id')
            for camper in campers:
                camper = Camper.objects.get(pk=camper)
                camper.new_class = group
                camper.save()
        elif request.POST['group-type'] == 'campers-only':
            first = request.POST.getlist('c-first-name')
            last = request.POST.getlist('c-last-name')
            father = request.POST.getlist('c-father-email')
            mother = request.POST.getlist('c-mother-email')
            for i in range(len(first)):
                if first[i] != '':
                    camper = Camper(
                        program=program,
                        first_name=first[i].title(), 
                        last_name=last[i].title(), 
                        father_email=father[i], 
                        mother_email=mother[i]
                    )
                    camper.save()

        return HttpResponseRedirect(reverse('index'))
