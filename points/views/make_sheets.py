import re
from django.shortcuts import HttpResponseRedirect, render #type: ignore
from django.urls import reverse #type: ignore

from points.models import Group, Task, BlankSheetLine #type: ignore
from points.wrappers import admin_only #type: ignore
      

@admin_only
def make_sheets(request):
    program = request.user.program
    if request.method == 'GET':
        bunks = program.group.filter(group_type='bunk').order_by('number')
        classes = program.group.filter(group_type='learning_class').order_by('number')

        bunks = {bunk: bunk.get_blank_sheet() for bunk in bunks}
        classes = {learning_class: learning_class.get_blank_sheet() for learning_class in classes}

        info = request.user.program.info.first()
        bunk_max = info.max_bunk_points
        class_max = info.max_class_points

        # TODO - this is a bit of a mess, and should be refactored, preferably into a method on the model
        general = {
            'bunk_master': program.get_tasks('bunk').filter(is_generic=True),
            'bunk_generic': program.create_and_get_blanksheet('bunk').filter(is_generic=True),
            'class_master': program.get_tasks('learning_class').filter(is_generic=True),
            'class_generic': program.create_and_get_blanksheet('learning_class').filter(is_generic=True),
        }
        
        return render(request, 'points/make_sheets.html', {
            'program': program,
            'bunk_tasks': program.task.filter(task_type='bunk', is_generic=True),
            'class_tasks': program.task.filter(task_type='learning_class', is_generic=True),
            'bunks': bunks,
            'classes': classes,
            'general': general,
            'bunk_max': bunk_max,
            'class_max': class_max,
        })

    elif request.method == 'POST':
        if request.POST['action'] == 'masterlist':

            task_type = request.POST['list_for']
            is_generic = True

            task_ids = request.POST.getlist('task-line-id')
            task_actions = request.POST.getlist('task-action')
            task_sequence = request.POST.getlist('task-sequence')
            task_names = request.POST.getlist('task-name')
            task_points = request.POST.getlist('task-points')

            for i, task in enumerate(task_ids):
                if task_actions[i] == 'delete':
                    task = Task.objects.get(id=task)
                    task.delete()
                elif task_actions[i] == 'edit':
                    task = Task.objects.get(id=task)
                    task.name = task_names[i]
                    task.max_points = task_points[i]
                    task.sequence = task_sequence[i]
                elif task_actions[i] == 'create':
                    if task_names[i] != '':
                        task_name = task_names[i].strip()
                        task = Task(
                            program=program, 
                            name=task_name.capitalize(), 
                            max_points=task_points[i],
                            task_type=task_type,
                            is_generic=is_generic,
                            sequence=task_sequence[i],
                        )
                if task:
                    task.save()

            # run the resequence method on the tasks
            program.resequence_tasks(task_type=task_type)

        elif request.POST['action'] in ['bunk', 'learning_class']:
            print(request.POST)
            group = request.POST['name']
            task_type = request.POST['action']
            if 'generic' in group:
                group = None
                is_generic = True
            else:
                group = program.group.get(id=group)
                is_generic = False
                group.use_generic_sheet = False
                group.save()
                if f'group-{group.id}-use-generic' in request.POST:
                    group.use_generic_sheet = True
                    group.save()
                    return HttpResponseRedirect(reverse('make_sheets'))
                
            task_ids = request.POST.getlist('task-line-id')
            task_names = request.POST.getlist('task-name')
            task_actions = request.POST.getlist('task-action')
            task_active = request.POST.getlist('task-active')
            task_sequence = request.POST.getlist('task-sequence')
            task_points = request.POST.getlist('task-points')
            task_input_type = request.POST.getlist('task-input-type')
            print(task_ids)
            for i, task_id in enumerate(task_ids):
                print(task_id)
                print(task_names[i])
                print(task_actions[i])
                print(task_active[i])
                print(task_sequence[i])
                print(task_points[i])
                print(task_input_type[i])

                if task_actions[i] == 'create':
                    task = Task(
                        program=program,
                        group=group,
                        name=task_names[i].capitalize(), 
                        max_points=task_points[i],
                        task_type=task_type,
                        is_generic=is_generic,
                        sequence=task_sequence[i],
                    )
                    task.save()
                else:
                    task = Task.objects.get(id=task_id)
                
                args = {
                    'task': task,
                    'program': program,
                    'group': group,
                    'is_generic': is_generic,
                    'group_type': request.POST['action'],
                    'max_points': task_points[i],
                    'points_type': task_input_type[i],
                    'sequence': task_sequence[i],
                    'active': task_active[i],
                }
                if program.blank_sheet.filter(task=task, group=group).exists():
                    line = program.blank_sheet.get(task=task, group=group)
                else:
                    line = BlankSheetLine()
                for key, value in args.items():
                    line.__setattr__(key, value)
                line.is_checklist_dict_updated = False
                line.save()

            group.reset_sequence()
                
        return HttpResponseRedirect(reverse('make_sheets'))