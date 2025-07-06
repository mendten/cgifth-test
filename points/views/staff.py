from django.shortcuts import render, redirect #type: ignore
from django.contrib.auth.decorators import login_required #type: ignore
from django.urls import reverse #type: ignore


from datetime import date
from pyluach import parshios, dates


@login_required
def staff(request):
    if request.user.position == 'admin':
        return redirect(reverse('index'))

    program = request.user.program
    group = request.user.group.first()

    parsha = parshios.getparsha_string(dates.HebrewDate.today())
    # get dates for the week using datetime
    today = date.today()
    week = program.get_week('number', today)
    charts = False
    week_chart = False
    if week not in ['before', 'after']:
        try:
            charts = group.get_four_charts(today)
            week_chart = group.get_weekly_charts(week, today)
        except Exception as e:
            print(e)
            charts = None
            week_chart = None

    info = program.info.first()
    ranks = program.rank.all()
    headers = ['Name', f'Counselor pts week {week}', f'LT pts week {week}', 'Overall counselor pts', 'Overall LT PTS',  'TOTAL pts', 'rank', 'pts to next rank']

    if request.user.position == 'counselor':
        max_bonus = info.max_bunk_bonus
    else:
        max_bonus = info.max_class_bonus
        
    return render(request, 'points/index_staff.html', {
        'group': group,
        'messages': request.user.get_messages(),
        'parsha': parsha,
        'charts': charts,
        'max_bonus': max_bonus,
        'week_chart': week_chart,
        'headers': headers,
    })
