from django.db import models


class MarkedSheetLine(models.Model):
    __name__ = 'MarkedSheetLine'

    points_type_choices = [
        ('custom', 'custom'),
        ('checkbox', 'checkbox'),
    ]

    sheet = models.ForeignKey('MarkedSheet', on_delete=models.CASCADE, related_name='line')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='line')
    camper = models.ForeignKey('Camper', on_delete=models.CASCADE, related_name='line')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='line')
    points_type = models.CharField(max_length=20, default='custom', choices=points_type_choices)
    points = models.IntegerField()
    max_points = models.IntegerField()
    date = models.DateField()
    week = models.IntegerField()
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.sheet} {self.task} {self.points}'
    
    def reset_sequence(self):
        if self.sequence == 0:
            blank_line = self.group.sheet.get(task=self.task)
            self.sequence = blank_line.sequence

    
    def save(self, *args, **kwargs):
        if not self.max_points:
            self.max_points = self.task.max_points
        if self.sequence == 0:
            self.reset_sequence()
        super().save(*args, **kwargs)
