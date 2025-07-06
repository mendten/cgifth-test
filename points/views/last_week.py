from django.shortcuts import render #type: ignore
from django.contrib.auth.decorators import login_required #type: ignore

from datetime import date, timedelta

from points.models import Info #type: ignore
from points.utils import get_range #type: ignore


@login_required
def last_week(request):
    if request.method == 'GET':

        program = request.user.program
        group = request.user.group.first()
        
        today = date.today()
        start_date = today - timedelta(days=7)


        charts = group.get_week_charts(today, start_date)
        info = Info.objects.all()[0]
        
        if request.user.position == 'counselor':
            max_bonus = info.max_bunk_bonus
        else:
            max_bonus = info.max_class_bonus

        return render(request, 'points/last_week.html', {
            'group': group,
            'charts': charts,
            'max_bonus': max_bonus,
        })
