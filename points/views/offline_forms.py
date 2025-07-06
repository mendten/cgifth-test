import json
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import date, datetime

from points.models import User,  Camper, MarkedSheet #type: ignore
from points.utils import get_rank #type: ignore


@csrf_exempt
def offline_forms(request):
    program = request.user.program
    data = json.loads(request.body)
    sheet_date = data['day']
    group = data['group']
    marker_id = data['marker']
    marker = User.objects.get(pk=marker_id)
    group_obj = marker.group.all()[0]
    campers = data['camper']
    tasks = data['tasks']
    tasks = tasks.lstrip("dict_keys(['").rstrip("'])").split("', '")
    tasks = ','.join(tasks) + ','
    sheet_date = datetime.strptime(sheet_date, '%Y-%m-%d')
    sheet_date = date(sheet_date.year, sheet_date.month, sheet_date.day)
    week = program.get_week('number', sheet_date)
    for camper in campers:
        if camper == '':
            continue
        camper_obj = Camper.objects.get(pk=camper)
        try:
            sheet = MarkedSheet.objects.get(date=sheet_date, name=group, camper=camper_obj, week=week)
            original = sheet.total
            camper_obj.total_points -= original
        except MarkedSheet.DoesNotExist:
            sheet = MarkedSheet(date=sheet_date, name=group, camper=camper_obj, week=week)
        
        sheet.marker = marker
        if group_obj:
            sheet.group = group_obj
        else:
            sheet.group = camper_obj.new_bunk
        sheet.checklist = tasks
        points = data[f'{camper}-points']
        total = 0
        for point in points.split(','):
            if point != '':
                total += int(point)
        sheet.points = points
        sheet.total = total
        sheet.save()
        camper_obj.total_points += total
        camper_obj.rank = get_rank(camper_obj.total_points)
        camper_obj.save()
    return HttpResponse('', status=200)
