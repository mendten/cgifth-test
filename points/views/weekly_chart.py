from django.shortcuts import render #type: ignor

from datetime import date

from points.models import Group, Info #type: ignore
from points.wrappers import admin_only #type: ignore
      
# import logging
# logger = logging.getLogger(__name__)


@admin_only
def weekly_chart(request):
    program = request.user.program
    today = date.today()
    last = program.get_last_day()
    if 'week' in request.GET:
        week = request.GET['week']
    else:
        if today > last:
            today = last
            week = program.get_week('number', today)
        else:
            week = program.get_week('number', today)
            if week == 'before':
                return render(request, 'points/weekly_chart.html')
            else:
                week -= 1

    bunks = Group.objects.filter(group_type='bunk', program=program).order_by('number')

    info = request.user.program.info.first()
    # ranks = info.ranks_list()
    # points = info.points_to_rank_list()

    headers = ['Name', f'Counselor pts week {week}', f'LT pts week {week}', 'Overall counselor pts', 'Overall LT PTS',  'TOTAL pts', 'rank', 'pts to next rank']

    bunk_totals = {}
    for bunk in bunks:
        bunk_totals[bunk] = bunk.get_weekly_charts(week, today)
        # logger.info('chart created for ' + bunk.name)  
        
    return render(request, 'points/weekly_chart.html', {
        'bunk_totals': bunk_totals,
        'week': week,
        'headers': headers,
    })
