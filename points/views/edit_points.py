from django.shortcuts import render #type: ignore

from datetime import date, timedelta, datetime

from points.models import Group, Info #type: ignore
from points.utils import get_week_charts #type: ignore
from points.wrappers import admin_only #type: ignore


@admin_only
def edit_points(request):
    """Admin view to see bunk/learning class points for the week."""
    program = request.user.program
    bunks = program.group.filter(group_type='bunk').order_by('number')
    classes = program.group.filter(group_type='learning_class').order_by('number')
    info = request.user.program.info.first()
    weeks = [info.start_date, info.week_1, info.week_2, info.week_3, info.week_4, info.week_5, info.week_6, info.week_7, info.week_8]
    charts = False
    group_obj = False
    staff = False
    current = True
    max_bonus = 0
    if 'id' in request.GET:
        group_id = request.GET['id']
        group_obj = Group.objects.get(pk=group_id)
        staff = group_obj.staff.all()

        if 'week' in request.GET:
            week = request.GET['week']
            week = datetime.strptime(week, '%Y-%m-%d')
            week = date(week.year, week.month, week.day)
        elif 'day' in request.GET:
            day = request.GET['day']
            day = datetime.strptime(day, '%Y-%m-%d')
            day = date(day.year, day.month, day.day)
            week = program.get_week('date', day)
        # find week in weeks list
        for i in range(len(weeks)):
            if week == weeks[i]:
                last_week = weeks[i-1]
                if i == 1:
                    last_week = last_week - timedelta(days=1)
                break

        charts = group_obj.get_week_charts(week, last_week)
        current = program.get_week('number', week)

        if group_obj.group_type == 'bunk':
            max_bonus = info.max_bunk_bonus
        else:
            max_bonus = info.max_class_bonus
        max_bonus = 100
        
    return render(request, 'points/edit_points.html', {
        'bunks': bunks,
        'classes': classes,
        'weeks': weeks,
        'charts': charts,
        'group': group_obj,
        'staff': staff,
        'current': current,
        'max_bonus': max_bonus,
    })