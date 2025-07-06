from django.db import models


class MarkedSheet(models.Model):
    __name__ = 'MarkedSheet'

    name = models.CharField(max_length=30)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='marked_sheet', blank=True, null=True)
    marker = models.ForeignKey('User', on_delete=models.PROTECT, related_name='sheet')
    camper = models.ForeignKey('Camper', on_delete=models.CASCADE, related_name='sheet')
    date = models.DateField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    max_points = models.IntegerField(blank=True, null=True)
    # TODO: store all the marked sheet lines in a dictionary that updates as the lines are modified
    # this is used to calculate the total points for the sheet
    # lines = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.date} {self.marker} {self.camper}'

    def set_total_points(self):
        self.total = sum([line.points for line in self.line.all()]) or 0
        self.max_points = sum([line.max_points for line in self.line.all()]) or 0 
        self.save()
        self.camper.set_total_points(points_type=self.name)

    def get_lines(self):
        return self.line.all()
    
