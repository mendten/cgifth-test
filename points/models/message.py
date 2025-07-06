from django.db import models


class Message(models.Model):
    __name__ = 'Message'

    group_choices = [
        ('counselor', 'counselor'),
        ('teacher', 'teacher'),
        ('all', 'all'),
    ]

    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='message', blank=True, null=True)
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='message_from')
    to = models.ManyToManyField('User', related_name='message_to')
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply', blank=True, null=True)
    group = models.CharField(choices=group_choices, max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.sender} {self.text}'