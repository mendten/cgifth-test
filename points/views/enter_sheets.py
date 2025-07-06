from django.shortcuts import HttpResponseRedirect, redirect #type: ignore
from django.contrib.auth.decorators import login_required #type: ignore
from django.urls import reverse #type: ignore

from datetime import date, datetime

from points.models import User, Camper, MarkedSheet, MarkedSheetLine, BlankSheetLine, Task#type: ignore
from points.utils import get_rank #type: ignore


@login_required
def enter_sheets(request):
    """Enter bunk/learning class points for a camper. Both staff view and admin view routes here."""
    program = request.user.program
    if request.method == 'POST':
        sheet_date = request.POST['day']
        group = request.POST['group']
        
        marker = request.user
        group_obj = program.group.get(id=group)
        group_type = group_obj.group_type.replace('_', ' ')

        campers = request.POST.getlist('camper')
        tasks = request.POST.getlist('task')

        sheet_date = datetime.strptime(sheet_date, '%Y-%m-%d')
        sheet_date = date(sheet_date.year, sheet_date.month, sheet_date.day)
        week = program.get_week('number', sheet_date)

        for camper in campers:
            any_changes = False
            if camper == '':
                continue
            camper_obj = Camper.objects.get(pk=camper)
            try:
                sheet = MarkedSheet.objects.get(
                    date=sheet_date, 
                    name=group_type, 
                    camper=camper_obj, 
                )
            except MarkedSheet.DoesNotExist:
                sheet = MarkedSheet(
                    date=sheet_date, 
                    name=group_type, 
                    camper=camper_obj, 
                    week=week
                )
            sheet.marker = marker
            sheet.group = group_obj
            sheet.save()
            for task in tasks:

                if task == '':
                    continue

                task_obj = Task.objects.get(pk=task)
                blank_line_obj = BlankSheetLine.objects.get(group=group_obj, task=task_obj)
                points = request.POST[f'camper-{camper}-task-{task}']

                if points == '':
                    points = 0
                else:
                    points = int(points)
                try:
                    line = MarkedSheetLine.objects.get(
                        sheet=sheet, 
                        task=task_obj
                    )
                except MarkedSheetLine.DoesNotExist:
                    line = MarkedSheetLine(
                        sheet=sheet,
                        task=task_obj,
                    )
                if line.points == points:
                    continue
                any_changes = True
                line.sheet = sheet
                line.group = group_obj
                line.camper = camper_obj
                line.task = task_obj
                line.points_type = blank_line_obj.points_type
                line.points = points
                line.max_points = blank_line_obj.max_points
                line.date = sheet_date
                line.week = week
                line.sequence = blank_line_obj.sequence
                line.save()
            if any_changes:
                sheet.set_total_points()
            # camper_obj.total_points += total
            # camper_obj.rank = get_rank(camper_obj.total_points)
            camper_obj.save()
        page = request.POST['from']
        if page == 'edit-points':
            return redirect(request.META['HTTP_REFERER'])
        return HttpResponseRedirect(reverse(page))
