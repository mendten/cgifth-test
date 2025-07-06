from django.db import models
from django.db.models import Q, Sum #type: ignore


class Camper(models.Model):
    __name__ = 'Camper'

    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='camper', blank=True, null=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=20)
    father_email = models.EmailField(blank=True)
    mother_email = models.EmailField(blank=True)
    new_bunk = models.ForeignKey('Group', on_delete=models.SET_NULL, related_name='bunk_camper', blank=True, null=True)
    new_class = models.ForeignKey('Group', on_delete=models.SET_NULL, related_name='class_camper', blank=True, null=True)
    total_points = models.IntegerField(default=0)
    total_bunk_points = models.IntegerField(default=0)
    total_class_points = models.IntegerField(default=0)
    rank = models.ForeignKey('Rank', on_delete=models.SET_NULL, blank=True, null=True)
    profile_pic = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_detailed_points(self, task_types, full_list, weeks):
        camper_totals = {}
        camper_totals['total'] = 0
        if task_types == 'all' or task_types == 'specific':
            sheets = self.sheet.filter(week__in=weeks)
        elif task_types == 'co_lt':
            sheets = self.sheet.filter(name__in=['bunk', 'learning class'], week__in=weeks)
        elif task_types == 'learning+class':
            sheets = self.sheet.filter(name='learning class', week__in=weeks)
        else:
            sheets = self.sheet.filter(name=task_types, week__in=weeks)
        sheets = sheets.order_by('date')
        for sheet in sheets:
            sheet_lines = sheet.line.all()
            # loop through each line and add to total
            if task_types != 'specific':
                print(sheet)
                camper_totals['total'] += sheet.total
            else:
                for line in sheet_lines:
                    if line.task in full_list:
                        if line.task not in camper_totals:
                            camper_totals[line.task] = 0
                        print(line)
                        # camper_totals[line.task] += int(line.points)
                        camper_totals['total'] += int(line.points)    
        return camper_totals
    
    def get_sheet(self, group, date):
        sheets = self.sheet.filter(Q(date=date) & Q(name=group))
        if sheets.exists():
            return sheets.get().total
        else:
            return 0
        
    def get_rank(self):
        ranks = self.program.rank.all()
        for rank in ranks:
            if self.total_points >= rank.lower_bound and self.total_points <= rank.upper_bound:
                return rank

    def set_total_points(self, points_type=False):
        sheets = self.sheet.all()
        self.total_points = sheets.aggregate(Sum('total'))['total__sum'] or 0
        print(self.total_points)
        if not points_type:
            self.total_bunk_points = sheets.filter(name='bunk').aggregate(Sum('total'))['total__sum'] or 0
            self.total_class_points = sheets.filter(name='learning class').aggregate(Sum('total'))['total__sum'] or 0
        elif points_type == 'bunk':
            self.total_bunk_points = sheets.filter(name='bunk').aggregate(Sum('total'))['total__sum'] or 0
            print(self.total_bunk_points)
        elif points_type in ['class', 'learning class']:
            self.total_class_points = sheets.filter(name='learning class').aggregate(Sum('total'))['total__sum'] or 0
            print(self.total_class_points)
        self.rank = self.get_rank()
        self.save()

    def profile_link(self):
        if self.last_name != '':
            return f'{self.id}x{self.last_name[0]}'
        elif self.first_name != '':
            return f'{self.id}x{self.first_name[0]}'
        else:
            return f'{self.id}'

    def save(self, *args, **kwargs):
        charts = self.weekly_chart.all()
        for chart in charts:
            chart.generate_chart()
        super(Camper, self).save(*args, **kwargs)
