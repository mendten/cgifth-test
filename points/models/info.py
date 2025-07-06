from django.db import models
from datetime import date

class Info(models.Model):
    __name__ = 'Info'

    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='info', blank=True, null=True)
    max_bunk_points = models.IntegerField()
    max_bunk_bonus = models.IntegerField()
    max_class_points = models.IntegerField()
    max_class_bonus = models.IntegerField()
    ranks = models.CharField(max_length=120, blank=True)
    points_to_rank = models.CharField(max_length=75, blank=True)
    start_date = models.DateField(blank=True, null=True)
    week_1 = models.DateField(blank=True, null=True)
    week_2 = models.DateField(blank=True, null=True)
    week_3 = models.DateField(blank=True, null=True)
    week_4 = models.DateField(blank=True, null=True)
    week_5 = models.DateField(blank=True, null=True)
    week_6 = models.DateField(blank=True, null=True)
    week_7 = models.DateField(blank=True, null=True)
    week_8 = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.program.name} Info'
    
    def get_week(self, type, date):
        if date < self.start_date:
            return 'before'
        
        weeks = {
            1: self.week_1,
            2: self.week_2,
            3: self.week_3,
            4: self.week_4,
            5: self.week_5,
            6: self.week_6,
            7: self.week_7,
            8: self.week_8
        }

        for week in weeks:
            try:
                if date <= weeks[week]:
                    if type == 'number':
                        return week
                    elif type == 'date':
                        return weeks[week]
            except:
                pass
        return 'after'

    def get_week_date(self, week):
        weeks = {
            1: self.week_1,
            2: self.week_2,
            3: self.week_3,
            4: self.week_4,
            5: self.week_5,
            6: self.week_6,
            7: self.week_7,
            8: self.week_8
        }
        return weeks[week]
    
    def set_defaults(self):

        today = date.today()
        self.max_bunk_points = 0
        self.max_bunk_bonus = 0
        self.max_class_points = 0
        self.max_class_bonus = 0
        self.start_date = today
        self.week_1 = today
        self.week_2 = today
        self.week_3 = today
        self.week_4 = today
        self.week_5 = today
        self.week_6 = today
        self.week_7 = today
        self.week_8 = today
        self.save()