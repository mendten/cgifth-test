from django import template

register = template.Library()

@register.inclusion_tag('points/reusables/daily_chart.html')
def daily_chart(request, date, chart, group):
    return {
        'request': request,
        'date': date,
        'chart': chart,
        'group': group,
    }