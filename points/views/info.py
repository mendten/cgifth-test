from django.shortcuts import HttpResponseRedirect, render #type: ignore
from django.urls import reverse #type: ignore

from points.models import *
from points.wrappers import admin_only #type: ignore


@admin_only
def info(request):
    program = request.user.program
    if not program.info.exists():
        info = Info(program=program)
        info.set_defaults()
    else:
        info = program.info.first()

    ranks = program.rank.all().order_by('lower_bound')
    if not ranks.exists():
        ranks = False


    if request.method == 'GET':
        weeks = [info.week_1, info.week_2, info.week_3, info.week_4, info.week_5, info.week_6, info.week_7, info.week_8]
        return render(request, 'points/info.html', {
            'info': info,
            'weeks': weeks,
            'ranks': ranks,
        })

    else:
        # save general info
        info.max_bunk_points = request.POST['max-bunk']
        info.max_bunk_bonus = request.POST['max-bunk-bonus']
        info.max_class_points = request.POST['max-class']
        info.max_class_bonus = request.POST['max-class-bonus']
        info.start_date = request.POST['start-date']
        info.week_1 = request.POST['week-1'] if request.POST['week-1'] != '' else None
        info.week_2 = request.POST['week-2'] if request.POST['week-2'] != '' else None
        info.week_3 = request.POST['week-3'] if request.POST['week-3'] != '' else None
        info.week_4 = request.POST['week-4'] if request.POST['week-4'] != '' else None
        info.week_5 = request.POST['week-5'] if request.POST['week-5'] != '' else None
        info.week_6 = request.POST['week-6'] if request.POST['week-6'] != '' else None
        info.week_7 = request.POST['week-7'] if request.POST['week-7'] != '' else None
        info.week_8 = request.POST['week-8'] if request.POST['week-8'] != '' else None
        info.save()

        # Create, update and delete existing ranks
        program.update_ranks(request.POST)


        return HttpResponseRedirect(reverse('info'))
