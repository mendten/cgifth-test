from .models import *
from .utils import *
from random import randint
from datetime import datetime, date, timedelta


def auto_input(num):
    day = date.today() - timedelta(days=num)
    if day.weekday() == 5:
        return
    week = program.get_week('number', day)
    groups = Group.objects.all()
    for group in groups:
        sheet = group.get_sheet()
        if group.group_type == 'bunk':
            campers = group.bunk_camper.all()
            name = 'bunk'
        else:
            name = 'learning class'
            campers = group.class_camper.all()
        markers = group.staff.all()
        for camper in campers:
            task_list = list(sheet.total_points())
            new = MarkedSheet(date=day, week=week, camper=camper)
            new.group = group
            new.name = name
            new.marker = markers[randint(0, len(markers) - 1)]
            tasks = ''
            points_list = ''
            total = 0
            for task, selected, points in task_list:
                if selected == 'True':
                    tasks += task + ','
                    num = randint(0, 10)
                    if num > 3:
                        total += int(points)
                        points_list += str(points) + ','
                    else:
                        points_list += '0,'
            tasks += 'bonus,'
            random_num = randint(0, 10)
            points_list += str(random_num) + ','
            total += random_num
            new.checklist = tasks
            new.points = points_list
            new.total = total
            new.save()


def update_to_today(option):
    """Function takes all marked sheets and updates their dates to closer to today, and updates session info to be around now."""
    if option == 'back':
        all = MarkedSheet.objects.all()
        for sheet in all:
            sheet.date = sheet.date - timedelta(weeks = 10)
            sheet.save()

        info = request.user.program.info.first()
        info.start_date = info.start_date - timedelta(weeks=10)

    elif option == 'forward':
        # get number of weeks to move forward. current date should the in middle of week 6
        info = request.user.program.info.first()
        week_5 = info.week_5
        today = date.today()
        # find first monday
        while today.weekday() != 0:
            today = today + timedelta(days=1)
        # get number of weeks between info.week_5 and today
        weeks_to_move = 0
        while week_5 < today:
            week_5 = week_5 + timedelta(weeks = 1)
            weeks_to_move += 1
        # move start date forward
        info.start_date = info.start_date + timedelta(weeks=weeks_to_move)
        info.save()
        # move all marked sheets forward
        all = MarkedSheet.objects.all()
        for sheet in all:
            sheet.date = sheet.date + timedelta(weeks=weeks_to_move)
            sheet.save()
        