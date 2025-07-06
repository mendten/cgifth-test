from django.shortcuts import render #type: ignore

from datetime import date, timedelta

from points.models import Group, MarkedSheet, Info #type: ignore
from points.wrappers import admin_only #type: ignore
      

@admin_only
def overall_points(request):
    program = request.user.program
    if request.method == 'GET':
        bunks = Group.objects.filter(group_type='bunk', program=program).order_by('number')
        program = request.user.program
        info = program.info.first()
        week_num = program.get_week('number', date.today())
        weeks = [info.week_1, info.week_2, info.week_3, info.week_4, info.week_5, info.week_6, info.week_7, info.week_8]
        # if week_num is None, set it to the last index of weeks that is not None
        if week_num is None or week_num == 'after':
            for i in range(len(weeks)):
                if weeks[i] is None:
                    week_num = i
                    break
                week_num = i + 1
        elif week_num == 'before':
            return render(request, 'points/overall_points.html', {
                'bunks': bunks,
                'camper_totals': False,
            })
        camper_totals = {}
        for bunk in bunks:
            camper_totals[bunk] = {}
            for i in range(week_num):
                camper_totals[bunk][i] = {}
                if i == 0:
                    days = [info.start_date + timedelta(days=x) for x in range((weeks[i] - info.start_date).days + 1)]
                else:
                    # days = all days from last week date + 1 to this week date
                    days = [(weeks[i - 1] + timedelta(days=1)) + timedelta(days=x) for x in range((weeks[i] - weeks[i - 1]).days)]
                camper_totals[bunk][i]['totals'] = {}
                # remove saturdays
                days = [day for day in days if day.weekday() != 5]
                camper_totals[bunk][i]['weekly'] = {}
                for camper in bunk.bunk_camper.all().order_by('last_name'):
                    camper_totals[bunk][i]['weekly'][camper] = {'co': 0, 'lt': 0}
                    camper_totals[bunk][i]['weekly'][camper]['camper'] = camper.sheet.get(name='camper', week=i+1).total if camper.sheet.filter(name='camper', week=i+1).exists() else 0
                for day in days:
                    if day > date.today():
                        continue
                    camper_totals[bunk][i][day] = {}
                    for camper in bunk.bunk_camper.all().order_by('last_name'):
                        camper_totals[bunk][i][day][camper] = {'co': 0, 'lt': 0}
                        camper_day_cell = camper_totals[bunk][i][day][camper]
                        camper_week_totals = camper_totals[bunk][i]['weekly'][camper]
                        try:
                            sheet = camper.sheet.get(name='bunk', date=day)
                            camper_day_cell['co'] = sheet.total
                            camper_week_totals['co'] += sheet.total
                            print('got a sheet')
                        except MarkedSheet.DoesNotExist:
                            camper_day_cell['co'] = ''
                            print('non-existent sheet dummy')
                        try:
                            sheet = MarkedSheet.objects.get(name='learning class', camper=camper, date=day)
                            camper_day_cell['lt'] = sheet.total
                            camper_week_totals['lt'] += sheet.total
                        except MarkedSheet.DoesNotExist:
                            camper_day_cell['lt'] = ''
                if i >= 0:
                    for camper in bunk.bunk_camper.all().order_by('last_name'):
                        if i > 0:
                            camper_totals[bunk][i]['totals'][camper] =  {'co': 0, 'lt': 0, 'camper': 0, 'total': 0}
                        else:
                            tot = camper_totals[bunk][i]['weekly'][camper]['co'] + camper_totals[bunk][i]['weekly'][camper]['lt'] + camper_totals[bunk][i]['weekly'][camper]['camper']
                            camper_totals[bunk][i]['totals'][camper] = {'total': int(tot)}
                            
                        camper_updated_totals = camper_totals[bunk][i]['totals'][camper]

                        if i == 1:
                            camper_updated_totals['co'] = camper_totals[bunk][i]['weekly'][camper]['co'] + camper_totals[bunk][i - 1]['weekly'][camper]['co']
                            camper_updated_totals['lt'] = camper_totals[bunk][i]['weekly'][camper]['lt'] + camper_totals[bunk][i - 1]['weekly'][camper]['lt']
                            camper_updated_totals['camper'] = camper_totals[bunk][i]['weekly'][camper]['camper'] + camper_totals[bunk][i - 1]['weekly'][camper]['camper']
                            camper_updated_totals['total'] = camper_updated_totals['co'] + camper_updated_totals['lt'] + camper_updated_totals['camper']
                        elif i > 1:
                            camper_updated_totals['co'] = camper_totals[bunk][i]['weekly'][camper]['co'] + camper_totals[bunk][i-1]['totals'][camper]['co']
                            camper_updated_totals['lt'] = camper_totals[bunk][i]['weekly'][camper]['lt'] + camper_totals[bunk][i-1]['totals'][camper]['lt']
                            camper_updated_totals['camper'] = camper_totals[bunk][i]['weekly'][camper]['camper'] + camper_totals[bunk][i-1]['totals'][camper]['camper']
                            camper_updated_totals['total'] = camper_updated_totals['co'] + camper_updated_totals['lt'] + camper_updated_totals['camper']
                
        return render(request, 'points/overall_points.html', {
            'bunks': bunks,
            'camper_totals': camper_totals,
        })
