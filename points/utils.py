from .models import *
from datetime import timedelta


# TODO: Make this whole method into a method on a model, most likely the Group model
def make_list(stats, request):
    pass
#     full_list = ['total']
#     if stats in ['all', 'bunk', 'co_lt']:
#         task_list = BlankSheet.objects.get(name='bunk master').checklist_list()
#         full_list.extend(task_list)
#     if stats in ['all', 'learning class', 'co_lt']:
#         task_list = BlankSheet.objects.get(name='learning class master').checklist_list()
#         full_list.extend(task_list)
#     if stats in ['all', 'camper']:
#         full_list.extend(['mission'])
#     if stats == 'specific':
#         full_list.extend(request.GET.getlist('tasks'))
#     if stats not in ['camper', 'specific']:
#         full_list.append('bonus')
#     return full_list


def get_four(user, day):
    """Makes a list of today, tomorrow, and the last 2 days to pass to the actual charts function. Skips saturdays."""
    start = day - timedelta(days=2)
    end = day + timedelta(days=2)
    days = [start + timedelta(days=i) for i in range((end - start).days)]
    # if any of the days are saturday, replace it
    for i in range(len(days)):
        if days[i].weekday() == 5:
            if i == 0:
                days[i] = days[i] - timedelta(days=1)
            elif i == 3:
                days[i] = days[i] + timedelta(days=1)
            elif i == 1:
                temp = days[0]
                days[0] = days[i] - timedelta(days=2)
                days[i] = temp
            elif i == 2:
                temp = days[3]
                days[3] = days[i] + timedelta(days=2)
                days[i] = temp

    charts = actual_charts(user, days)
    return charts


def get_range(user, day):
    """Gets a list for the last 7 days to pass to the actual charts function. Skips saturdays."""
    start = day - timedelta(days=8)
    end = day
    days = [start + timedelta(days=i) for i in range((end - start).days)]
    # if any of the days are saturday, remove it
    for day in days:
        if day.weekday() == 5:
            days.remove(day)

    charts = actual_charts(user, days)
    return charts


def get_week_charts(week, last_week, markers):
    """Gets the charts for the given week."""
    start = last_week + timedelta(days=1)
    end = week + timedelta(days=1)
    days = [start + timedelta(days=i) for i in range((end - start).days)]
    # if any of the days are saturday, remove it
    for day in days:
        if day.weekday() == 5:
            days.remove(day)

    charts = actual_charts(markers[0], days)
    return charts


def actual_charts(user, days):
    """"Gets the actual charts for the given days."""
    info = user.program.info.first()
    charts = {day: {} for day in days}
    group = user.group.first()
    # get max bonus amount for group type
    if group.group_type == 'bunk':
        max_bonus = info.max_bunk_bonus
    elif group.group_type == 'learning class':
        max_bonus = info.max_class_bonus
    for day in days:
        if MarkedSheet.objects.filter(date=day, group=group).exists():
            sheets = MarkedSheet.objects.filter(date=day, group=group).order_by('camper__last_name')
            task_list = sheets[0].checklist_list()
            full_list = list(group.get_sheet().total_points())
            charts[day]['tasks'] = {}
            for task, _, points in full_list:
                if task in task_list:
                    charts[day]['tasks'][task] = points
            charts[day]['tasks']['bonus'] = 'max: ' + str(max_bonus)
            for sheet in sheets:
                charts[day][sheet.camper] = dict(sheet.total_points())
                if 'bonus' in charts[day][sheet.camper]:
                    temp = charts[day][sheet.camper]['bonus']
                    charts[day][sheet.camper]['bonus'] = {'bonus': temp}
            
        else:
            charts[day]['tasks'] = {}
            blank = group.get_sheet()
            data = blank.total_points()
            unzipped = list(data)
            blank_list = {}
            for task, selected, points in unzipped:
                if selected == 'True':
                    charts[day]['tasks'][task] = points
                    blank_list[task] = '0'
            charts[day]['tasks']['bonus'] = 'max: ' + str(max_bonus)
            blank_list['bonus'] = {'bonus': '0'}
            if group.group_type == 'bunk':
                campers = group.bunk_camper.all().order_by('last_name')
            elif group.group_type == 'learning class':
                campers = group.class_camper.all().order_by('last_name')
            for camper in campers:
                charts[day][camper] = blank_list

    return charts
            

def get_rank(num):
    info = Info.objects.first()
    stuff = info.ranks_and_points()
    for rank, points in dict(stuff).items():
        lower, upper = points.split('-')
        if num >= int(lower) and num <= int(upper):
            return rank


def create_profile(camper):
    """Creates a profile for the given camper."""
    temp = {}
    rank = camper.rank
    points = camper.total_points
    ptnr = 0
    while True:
        next_rank = get_rank(points + ptnr)
        if next_rank != rank:
            break
        ptnr += 1
    temp['next_rank'] = next_rank
    temp['ptnr'] = ptnr

    stats = {}

    sheets = MarkedSheet.objects.filter(camper=camper)
    for sheet in sheets:
        if sheet.name in ['bunk', 'learning class']:
            for task, point in dict(sheet.total_points()).items():
                if task not in stats:
                    stats[task] = {'max': 1, 'done': 0, 'points': int(point)}
                else:
                    stats[task]['max'] += 1
                    stats[task]['points'] += int(point)
                if int(point) > 0:
                    stats[task]['done'] += 1
    for task in stats:
        stats[task]['percent'] = round(stats[task]['done'] / stats[task]['max'] * 100)

    temp['stats'] = stats

    # remove bonus from stats
    if 'bonus' in stats:
        del stats['bonus']
    
    return temp