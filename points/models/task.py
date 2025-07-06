from django.db import models


class Task(models.Model):
    __name__ = 'Task'

    task_type_choices = [
        ('bunk', 'bunk'),
        ('learning_class', 'learning_class'),
        ('camper', 'camper'),
    ]

    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='task', blank=True, null=True)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, blank=True)
    task_type = models.CharField(choices=task_type_choices, max_length=30)
    sequence = models.IntegerField(blank=True, null=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='task', blank=True, null=True)
    max_points = models.IntegerField(blank=True, null=True)
    is_generic = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.name}'
    
    
    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.name
        if not self.max_points:
            self.max_points = -1
        if not self.sequence:
            self.sequence = 0
        if self.group:
            self.is_generic = False
        super().save(*args, **kwargs)