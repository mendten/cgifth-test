from django.shortcuts import render #type: ignore

from points.models import * #type: ignore
from points.utils import make_list
from points.wrappers import admin_only #type: ignore
      

@admin_only
def detail_points(request):
    program = request.user.program
    # TODO: Refactor this entire. Should move most of the logic to the models
    if request.method == 'GET':

        # get a list of all bunks and all classes
        groups = program.group.all().order_by('group_type', 'number')

        # create a variable in which we will store all of the camper points
        camper_totals = False

        # create a variable in which we will store the list of tasks
        full_list = False

        # create a variable for something
        current_selection = False

        # create a dict in which we will store all of the tasks for the user to select, then get all tasks and them to the list
        task_selector = {}
        tasks = Task.objects.all().order_by('sequence')
        for task in tasks:
            task_selector[task.id] = task.name

        if 'group-type' in request.GET:
            print(request.GET)
            # get the group type (either bunk, class, or individual campers)
            group = request.GET['group-type']

            # get the type of tasks to look at. Could be bunk, class, weekly mission, specific tasks...
            task_types = request.GET['stat-type']

            # get the weeks to consider
            date_range = request.GET.getlist('range')
            if 'all' in date_range or not date_range:
                weeks = ['1', '2', '3', '4', '5', '6', '7', '8']
            else:
                weeks = date_range

            # get a list of tasks matching the provided critera
            full_list = program.get_task_list(task_types)

            # if we want tot view individual campers:    
            if group == 'indiv':
                # get all campers
                campers = program.camper.all()

                camper_totals = {}

                for camper in campers:
                    camper_totals[camper] = camper.get_detailed_points(task_types, full_list, weeks)

                camper_totals = sorted(camper_totals.items(), key=lambda x: x[1]['total'], reverse=True)

            elif group == 'bunk' or group == 'learning_class':
                groups = Group.objects.filter(group_type=group)
                
                full_list.insert(0, 'average')
                bunk_totals = {}
                for bunk in groups:
                    bunk_totals[bunk.name] = {'average': 0, 'total': 0} 

                    if bunk.group_type == 'bunk':
                        campers = bunk.bunk_camper.all()
                    else:
                        campers = bunk.class_camper.all()

                    if task_types == 'all' or task_types == 'specific':
                        sheets = MarkedSheet.objects.filter(camper__in=campers, week__in=weeks)
                    elif task_types == 'co_lt':
                        sheets = MarkedSheet.objects.filter(camper__in=campers, name__in=['bunk', 'learning class'], week__in=weeks)
                    elif task_types == 'learning class':
                        sheets = MarkedSheet.objects.filter(camper__in=campers, name='learning class', week__in=weeks)
                    else:
                        sheets = MarkedSheet.objects.filter(camper__in=campers, name=task_types, week__in=weeks)
                    for sheet in sheets:
                        lines = sheet.line.all()
                        # unzip tasks and points and add to camper_totals
                        for line in lines:
                            if line.task in full_list:
                                # bunk_totals[bunk.name][task] += int(points)
                                bunk_totals[bunk.name]['total'] += line.points
                    
                    bunk_totals[bunk.name]['average'] = float('{:.2f}'.format(bunk_totals[bunk.name]['total'] / campers.count()))
                camper_totals = sorted(bunk_totals.items(), key=lambda x: (x[1]['average'], x[1]['total']),  reverse=True)
            
            # delete everything from full_list besides total (and average)
            if task_types != 'specific':
                full_list = ['total']
                if group in ['bunk', 'learning_class']:
                    full_list.insert(0, 'average')

            current_selection = {'Type': group, 'Tasks': task_types, 'Weeks': weeks}

        return render(request, 'points/detail_points.html', {
            'groups': groups,
            'current_selection': current_selection,
            'task_selector': task_selector,
            'camper_totals': camper_totals,
            'full_list': full_list,
        })
