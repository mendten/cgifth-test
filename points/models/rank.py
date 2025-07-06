from django.db import models


class Rank(models.Model):
    __name__ = 'Rank'

    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='rank', blank=True, null=True)
    name = models.CharField(max_length=100)
    lower_bound = models.IntegerField()
    upper_bound = models.IntegerField()

    def __str__(self):
        return self.name