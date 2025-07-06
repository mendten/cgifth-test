from django.db import models
from django.db.models import Q

from datetime import date, timedelta, datetime


from .reports import WeeklyChart


class Group(models.Model):
    __name__ = 'Group'

    group_type_choices = [
        ('bunk', 'bunk'),
        ('learning_class', 'learning_class'),
    ]

    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='group', blank=True, null=True)
    name = models.CharField(max_length=30)
    group_type = models.CharField(choices=group_type_choices, max_length=30)
    number = models.IntegerField()
    staff = models.ManyToManyField('User', related_name='group', blank=True)
    use_generic_sheet = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}, {self.number}'
    
    def get_task_list(self):
        tasks = self.task.all()
        return tasks
    
    def get_blank_sheet(self, task_objects=False):
        print('getting blank sheet for ' + self.name)
        blank_lines = self.sheet.all().order_by('sequence')
        
        if task_objects:
            blank_lines = self.sheet.filter(active=True).order_by('sequence')
            return blank_lines
        
        task_list = []
        for task in blank_lines:
            if not task.is_checklist_dict_updated:
                task.set_checklist_dict()
                task.save()
            task_list.append(task.checklist_dict)
        return task_list
        # return self.program.create_and_get_blanksheet(group_type=self.group_type, group=self)

    def get_marked_sheet(self, date=False):
        if date:
            return self.marked_sheet.filter(date=date) if self.marked_sheet.filter(date=date).exists() else False
        return self.marked_sheet.all()
    
    def reset_sequence(self):
        blank_lines = self.sheet.all().order_by('sequence',)
        for i, line in enumerate(blank_lines):
            line.sequence = i
            line.save()

    def get_four_charts(self, day):
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

        charts = self.actual_charts(days)
        return charts
    
    def get_week_charts(self, week, last_week):
        """Gets the charts for the given week."""
        start = last_week + timedelta(days=1)
        end = week + timedelta(days=1)
        days = [start + timedelta(days=i) for i in range((end - start).days)]
        # if any of the days are saturday, remove it
        for day in days:
            if day.weekday() == 5:
                days.remove(day)

        charts = self.actual_charts(days)
        return charts

    
    def actual_charts(self, days):
        """Gets the actual charts for the given days."""
        info = self.program.info.first()
        charts = {day: {} for day in days}

        today = datetime.today()
        today = date(today.year, today.month, today.day)

        # get max bonus amount for group type
        if self.group_type == 'bunk':
            max_bonus = info.max_bunk_bonus
            campers = self.bunk_camper.all().order_by('last_name')
        elif self.group_type == 'learning_class':
            max_bonus = info.max_class_bonus
            campers = self.class_camper.all().order_by('last_name')

        for day in days:

            if self.get_marked_sheet(date=day):
                sheets = self.get_marked_sheet(date=day)
                sheets = sheets.order_by('camper__last_name')
                charts[day]['tasks'] = {}
                for line in sheets[0].line.all().order_by('sequence'):
                    charts[day]['tasks'][line.task] = line

                charts[day]['tasks']['bonus'] = 'max: ' + str(max_bonus)
                for sheet in sheets:
                    charts[day][sheet.camper] = {}
                    for line in sheet.line.all().order_by('sequence'):
                        charts[day][sheet.camper][line.task] = line

                total = sum(sheet.total for sheet in sheets)
                max_points = sum(sheet.max_points for sheet in sheets)
                
                try:
                    charts[day]['total'] = round((total / max_points) * 100)
                except ZeroDivisionError:
                    charts[day]['total'] = 0

                if day < today and charts[day]['total'] == 0:
                    charts[day]['total'] = 'late'

            else:
                charts[day]['tasks'] = {}
                blank_sheet_lines = self.get_blank_sheet(task_objects=True)
                for line in blank_sheet_lines:
                    charts[day]['tasks'][line.task] = line
                charts[day]['tasks']['bonus'] = 'max: ' + str(max_bonus)
                for camper in campers:
                    charts[day][camper] = {}
                    for line in blank_sheet_lines:
                        charts[day][camper][line.task] = line

                if day < today:
                    charts[day]['total'] = 'late'

            if day == today:
                charts[day]['today'] = True
            
        return charts


    def get_weekly_charts(self, week, today):
        """Gets the weekly chart for the given group and week."""
        headers = ['Name', f'Counselor Pts Week {week}', f'Lt Pts Week {week}', 'Overall Counselor Points', 'Overall Lt Points', 'Total Pts', 'Rank', 'Pts To Next Rank']
        charts = []
        if self.group_type == 'bunk':
            campers = self.bunk_camper.all().order_by('last_name')
        else:
            campers = self.class_camper.all().order_by('last_name')

        for camper in campers:
            try:
                chart = camper.weekly_chart.get(week=week, group=self)
            except WeeklyChart.DoesNotExist:
                chart = WeeklyChart(
                    program=self.program,
                    week=week,
                    group=self,
                    camper=camper
                )
                chart.generate_chart(week)
            ordered_chart = {key: chart.chart[key] for key in headers}
            charts.append(ordered_chart)
        print(charts)
        return charts
    
