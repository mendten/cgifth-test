from django.db import models

from datetime import date, timedelta

from .rank import Rank


class Program(models.Model):
    __name__ = 'Program'

    name = models.CharField(max_length=100)
    admin = models.ForeignKey('User', on_delete=models.SET_NULL, related_name="program_admin",blank=True, null=True)
    staff = models.ManyToManyField('User', related_name='program_staff', blank=True)


    def __str__(self):
        return self.name
    
    def get_week(self, type, date):
        if not self.info.exists():
            return {'Error': 'Info has not been configured yet. Please configure the info for this program.'}
        
        info = self.info.first()
        return info.get_week(type, date)

    def get_last_day(self):
        """Returns the last day of camp"""
        info_obj = self.info.first()
        weeks = {
            1: info_obj.week_1,
            2: info_obj.week_2,
            3: info_obj.week_3,
            4: info_obj.week_4,
            5: info_obj.week_5,
            6: info_obj.week_6,
            7: info_obj.week_7,
            8: info_obj.week_8
        }
        for week in reversed(weeks):
            if weeks[week] is not None:
                return weeks[week]
    
    def create_ranks(self, titles, lower_bounds, upper_bounds):
        ranks = []
        for i in range(len(titles)):
            if titles[i] == '' or lower_bounds[i] == '' or upper_bounds[i] == '':
                continue
            rank = Rank(program=self, name=titles[i], lower_bound=lower_bounds[i], upper_bound=upper_bounds[i])
            rank.save()
            ranks.append(rank)
        return ranks
    
    def update_ranks(self, post):
        titles = post.getlist('new-rank-title')
        lower_bounds = post.getlist('new-rank-lower')
        upper_bounds = post.getlist('new-rank-upper')
        self.create_ranks(titles, lower_bounds, upper_bounds)

        existing_ranks = post.getlist('rank-id')
        for id in existing_ranks:
            rank = Rank.objects.get(id=id)
            name = post.get(f'rank-{id}')
            lower_bound = post.get(f'lower-{id}')
            upper_bound = post.get(f'upper-{id}')
            if name == '' or lower_bound == '' or upper_bound == '':
                rank.delete()
                continue
            rank.name = name
            rank.lower_bound = lower_bound
            rank.upper_bound = upper_bound
            rank.save()

        return True
    
    def chart_checker(self, day, groups):
        """Checks to see if any charts were submitted for the last three days."""
        last_3 = [day - timedelta(days=i) for i in range(3)]
        last_3.reverse()
        # if any of the days are saturday, drop it
        for i in range(len(last_3)):
            if last_3[i].weekday() == 5:
                # add a day at the beginning
                last_3.insert(0, last_3[0] - timedelta(days=1))
                last_3.pop(i + 1)
                break
        days = {day: {} for day in last_3}
        for day in days:
            for group in groups:
                days[day][group] = False
                total = 0
                max_points = 0
                if group.marked_sheet.filter(date=day).exists():
                    # check to see if there are any points
                    sheets = group.marked_sheet.filter(date=day)
                    for sheet in sheets:
                        # sheet.set_total_points()
                        total += sheet.total
                        max_points += sheet.max_points
                    try:
                        # get the percantage of points earned, and format it to a percentage
                        days[day][group] = round((total / max_points) * 100) 
                    except ZeroDivisionError:
                        days[day][group] = 0

        return days
    
    def get_tasks(self, task_type=False):
        """Returns a list of tasks for a program"""
        if task_type:
            tasks = self.task.filter(task_type=task_type).order_by('sequence')
        else:
            tasks = self.task_task.all().order_by('sequence')
        return tasks
    
    def get_task_list(self, task_types=False, task_id_list=False):
        full_list = ['total']
        if task_types in ['all', 'bunk', 'co_lt']:
            task_list = self.task.filter(task_type='bunk').order_by('sequence')
            full_list.extend(task_list)
        if task_types in ['all', 'learning class', 'co_lt']:
            task_list = self.task.filter(task_type='learning_class').order_by('sequence')
            full_list.extend(task_list)
        if task_types in ['all', 'camper']:
            task_list = self.task.filter(task_type='camper').order_by('sequence')
            full_list.extend(task_list)
        if task_types == 'specific':
            task_list = self.task.filter(pk__in=task_id_list)
            full_list.extend(task_list)
        if task_types not in ['camper', 'specific']:
            task_list = self.task.filter(name='bonus')
            if task_list:
                full_list.append(task_list)
        return full_list

    def resequence_tasks(self, task_type=None, group=None):
        tasks = self.task.filter(task_type=task_type)
        if group:
            tasks = tasks.filter(group=group)
        for i, task in enumerate(tasks):
            task.sequence = i
            task.save()

    def create_and_get_blanksheet(self, group_type, group=None):
        tasks = self.get_tasks(task_type=group_type)
        if not group:
            tasks = tasks.filter(group=None)
        for task in tasks:
            if not self.blank_sheet.filter(task=task, group_type=group_type, group=group).exists():
                new_sheet = self.blank_sheet.create(
                    program=self,
                    group_type=group_type,
                    group=group,
                    task=task,
                    max_points=task.max_points,
                    sequence=task.sequence,
                    active=False,
                )
            else:
                new_sheet = self.blank_sheet.filter(task=task, group_type=group_type, group=group).first()
            if group and group.use_generic_sheet:
                generic_task = self.blank_sheet.filter(task=task, group_type=group_type, group=None).first()
                if generic_task:
                    new_sheet.max_points = generic_task.max_points
                    new_sheet.active = generic_task.active
                    new_sheet.points_type = generic_task.points_type
            new_sheet.save()
        return self.blank_sheet.filter(group_type=group_type, group=group).order_by('sequence')
        