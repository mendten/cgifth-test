from django.db import models


class BlankSheetLine(models.Model):
    __name__ = 'BlankSheetLine'

    points_type_choices = [
        ('custom', 'custom'),
        ('checkbox', 'checkbox'),
    ]

    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='blank_sheet', blank=True, null=True)
    is_generic = models.BooleanField(default=False)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='sheet', blank=True, null=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='sheet')
    group_type = models.CharField(max_length=30, default='bunk', choices=[('bunk', 'bunk'), ('learning_class', 'learning_class'), ('camper', 'camper')])
    points_type = models.CharField(max_length=20, default='custom', choices=points_type_choices)
    max_points = models.IntegerField(default=-1)
    sequence = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    checklist_dict = models.JSONField(blank=True, null=True)
    is_checklist_dict_updated = models.BooleanField(default=False)

    def __str__(self):
        if not self.group:
            return f'Generic {self.task}'
        return f'{self.group} {self.task}'
    
    def set_checklist_dict(self):
        print('getting dict', self.task.name, self.group)
        data = {
            'name': self.task.name,
            'task_id': self.task.id,
            'group': self.group.name if self.group else 'Generic',
            'max_points': self.max_points,
            'points_type': self.points_type,
            'sequence': self.sequence,
            'active': self.active,
        }
        self.checklist_dict = data
        self.is_checklist_dict_updated = True

    def save(self, *args, **kwargs):
        if self.group:
            self.is_generic = False
        else:
            self.is_generic = True
        if not self.is_checklist_dict_updated:
            self.set_checklist_dict()
        super().save(*args, **kwargs)