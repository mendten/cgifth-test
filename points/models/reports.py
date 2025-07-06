from django.db import models
from django.db.models import Sum

from datetime import datetime, date

class WeeklyChart(models.Model):
    __name__ = "WeeklyChart"
    
    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='weekly_chart', blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='weekly_chart', blank=True, null=True)
    camper = models.ForeignKey('Camper', on_delete=models.CASCADE, related_name='weekly_chart', blank=True, null=True)
    chart = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ('program', 'week', 'group', 'camper')

    def __str__(self):
        return f'{self.group} {self.camper} {self.week}'


    def get_or_create(self, week=False):
        if not week:
            today = datetime.today()
            today = date(today.year, today.month, today.day)
            week = self.program.info.first().get_week('number', today)
        try:
            chart = WeeklyChart.objects.get(program=self.program, week=week, group=self.group, camper=self.camper)
        except WeeklyChart.DoesNotExist:
            chart = WeeklyChart(
                program=self.program,
                week=week,
                group=self.group,
                camper=self.camper
            )
            chart.generate_chart(week)
        return chart


    def generate_chart(self, week=False):

        if not week:
            today = datetime.today()
            today = date(today.year, today.month, today.day)
            week = self.program.info.first().get_week('number', today)
        if self.week:
            week = self.week

        headers = ['Name', f'Counselor Pts Week {week}', f'Lt Pts Week {week}', 'Overall Counselor Points', 'Overall Lt Points', 'Total Pts', 'Rank', 'Pts To Next Rank']

        chart = {
            'Name': f'{self.camper.last_name.title()}, {self.camper.first_name.title()}',
            f'Counselor Pts Week {week}': 0,
            f'Lt Pts Week {week}': 0,
            f'Overall Counselor Points': self.camper.total_bunk_points,
            f'Overall Lt Points': self.camper.total_class_points,
            'Total Pts': self.camper.total_points,
            'Rank': self.camper.rank.name if self.camper.rank else 'No Rank',
            'Pts To Next Rank': self.camper.rank.upper_bound - self.camper.total_points if self.camper.rank else 'N/A',
        }

        bunk_sheets = self.camper.sheet.filter(week=week, name='bunk')
        lt_sheets = self.camper.sheet.filter(week=week, name='learning class')
        chart[f'Counselor Pts Week {week}'] = bunk_sheets.aggregate(Sum('total'))['total__sum'] or 0
        chart[f'Lt Pts Week {week}'] = lt_sheets.aggregate(Sum('total'))['total__sum'] or 0

        ordered_chart = {key: chart[key] for key in headers}

        self.chart = ordered_chart
        print(chart)
        self.save()


class OverallPoints(models.Model):
    pass


class OverallPointsCamper(models.Model):
    pass