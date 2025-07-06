from django import template

register = template.Library()

@register.inclusion_tag('points/reusables/task_table.html')
def task_table(request, tasks, page, list_for=False):
    if not tasks:
        tasks = [_ + 1 for _ in range(30)]
    return {
        'tasks': tasks,
        'page': page,
        'list_for': list_for,
    }