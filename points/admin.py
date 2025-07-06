from django.contrib import admin
from .models import *


class MarkedSheetAdmin(admin.ModelAdmin):
    list_display = ('date', 'week', 'camper', 'total', 'group', 'marker',)
    list_filter = ('name', 'date', 'week', 'camper', 'group', 'marker', )


class BlankSheetLineAdmin(admin.ModelAdmin):
    list_display = ('group', 'task', 'max_points', 'sequence', 'active')
    list_filter = ('group', 'task')

class MarkedSheetLineAdmin(admin.ModelAdmin):
    list_display = ('group', 'task', 'points', 'camper', 'date')
    list_filter = ('group', 'task', 'camper', 'date')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('date',)


# Register your models here.
admin.site.register(Program)
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Camper)
admin.site.register(MarkedSheet, MarkedSheetAdmin)
admin.site.register(Info)
admin.site.register(Rank)
admin.site.register(Message, MessageAdmin)
admin.site.register(Task)
admin.site.register(MarkedSheetLine, MarkedSheetLineAdmin)
admin.site.register(BlankSheetLine, BlankSheetLineAdmin)
admin.site.register(WeeklyChart)