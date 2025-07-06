from django.shortcuts import render, redirect #type: ignore
from django.urls import reverse #type: ignore

from datetime import date, timedelta 

from points.models import *


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.position == 'admin':
            user = request.user
            program = user.program
            info_obj = program.info.first()
            today = date.today()
            status = program.get_week('number', today)
            # status = program.get_week('number', today, program)
            yesterday = False

            groups = program.group.all().order_by('group_type', 'number')

            error = False
            if type(status) == dict and 'Error' in status:
                error = status.get('Error')

            if status == 'after':
                # get the last day of camp
                yesterday = program.get_last_day()
            elif status != 'before':
                yesterday = today - timedelta(days=1)
            if yesterday:
                checker = program.chart_checker(yesterday, groups)
            else:
                checker = False

            return render(request, 'points/admin.html', {
                'error': error,
                'groups': groups,
                'chart_checker': checker,
            })
        else:
            return redirect(reverse('staff'))
    else:
        camper_totals = {}
        campers = Camper.objects.all()
        for camper in campers:
            camper_totals[camper] = {}
            camper_totals[camper]['rank'] = camper.rank
            camper_totals[camper]['points'] = camper.total_points

        camper_totals = sorted(camper_totals.items(), key=lambda x: x[1]['points'], reverse=True)
        camper_totals = camper_totals[:100]
        # sort camper_totals alphabetically 
        # Leibel wants it to be in order
        # camper_totals = sorted(camper_totals, key=lambda x: x[0].last_name)
        bunk_totals = {}
        bunks = Group.objects.filter(group_type='bunk')
        for bunk in bunks:
            bunk_totals[bunk] = {}
            bunk_totals[bunk]['points'] = 0
            bunk_totals[bunk]['average'] = 0
            for camper in bunk.bunk_camper.all():
                bunk_totals[bunk]['points'] += camper.total_points
            num_camper = bunk.bunk_camper.count()
            bunk_totals[bunk]['average'] = int(bunk_totals[bunk]['points'] / num_camper)
        bunk_totals = sorted(bunk_totals.items(), key=lambda x: x[1]['points'], reverse=True)

        return render(request, 'points/home.html', {
            'camper_totals': camper_totals,
            'bunk_totals': bunk_totals,
        })
