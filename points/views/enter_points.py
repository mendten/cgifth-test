from django.shortcuts import HttpResponseRedirect, render #type: ignore
from django.urls import reverse #type: ignore

from datetime import date

from points.models import Group, Camper, MarkedSheet, MarkedSheetLine, Task #type: ignore
from points.utils import get_rank #type: ignore
from points.wrappers import admin_only #type: ignore


@admin_only
def enter_points(request):
    """Admin view to enter Camper points for the week (not bunk/learning class)."""
    program = request.user.program
    if request.method == 'GET':

        try:
            tasks = program.task.get(name='Weekly Mission')
        except Task.DoesNotExist:
            tasks = Task(
                program=program,
                name='Weekly Mission', task_type='camper',
                is_generic=False,
                max_points=1000,
                sequence=-1)
            tasks.save()

        bunks = Group.objects.filter(group_type='bunk', program=program).order_by('number')
        # group = 'camper'
        info = request.user.program.info.first()
        weeks = [info.week_1, info.week_2, info.week_3, info.week_4, info.week_5, info.week_6, info.week_7, info.week_8]

        charts = {}
        for bunk in bunks:
            charts[bunk] = {}
            for week in weeks:
                week_number = program.get_week('number', week)
                charts[bunk][week_number] = {}
                for camper in bunk.bunk_camper.all():
                    charts[bunk][week_number][camper] = 2 * week_number


        return render(request, 'points/enter_points.html', {
            'bunks': bunks,
            'weeks': weeks,
            'charts': charts,
        })
    
    else:
        week = request.POST['week']
        marker = request.user
        campers = request.POST.getlist('camper')
        group = 'camper'
        weekly_mission_task = program.task.get(name='Weekly Mission')
        for camper in campers:
            camper_obj = Camper.objects.get(pk=camper)
            try:
                sheet = MarkedSheet.objects.get(name=group, camper=camper_obj, week=week)
            except MarkedSheet.DoesNotExist:
                sheet = MarkedSheet(date=date.today(), name=group, camper=camper_obj, week=week)
            sheet.group = camper_obj.new_bunk
            sheet.marker = marker
            try:
                sheet_line = sheet.line.get(task=weekly_mission_task)
            except:
                sheet_line = sheet.line.create(task=weekly_mission_task)
            sheet_line.points = request.POST[f'{camper}-points']
            sheet_line.save()
        return HttpResponseRedirect(reverse('enter_points'))
