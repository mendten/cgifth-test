from django.db import models
from django.contrib.auth.models import AbstractUser #type: ignore


# Create your models here.
class User(AbstractUser):
    __name__ = 'User'

    position_choices = [
        ('admin', 'admin'),
        ('counselor', 'counselor'),
        ('teacher', 'teacher'),
    ]

    program = models.ForeignKey('Program', on_delete=models.SET_NULL, related_name='user', blank=True, null=True)
    position = models.CharField(choices=position_choices, max_length=20)

    def __str__(self):
        return f'{self.first_name.title()} {self.last_name.title()}'

    def get_messages(self):
         return self.message_to.all() | self.message_from.all()

    # when a user is created, add to the program
    # if the user is an admin, set the program admin to the user
    def create_user(self, *args, **kwargs):
        super().create_user(*args, **kwargs)
        program = self.program
        if self.position == 'admin':
            program.admin = self
        else:
            program.staff.add(self)
        program.save()















