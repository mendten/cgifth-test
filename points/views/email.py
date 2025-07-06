from django.shortcuts import render #type: ignore
from django.contrib.auth import authenticate #type: ignore
from django.core.mail import send_mail #type: ignore
from django.conf import settings #type: ignore

from datetime import date, datetime

from points.models import Group, MarkedSheet, Info #type: ignore
from points.utils import get_rank #type: ignore
from points.wrappers import admin_only #type: ignore
    

@admin_only
def email(request):
    program = request.user.program
    today = date.today()
    last = program.get_last_day()
    if today > last:
        today = last
    week = program.get_week('number', today)
    info = program.info.first()
    weeks = [info.week_1, info.week_2, info.week_3, info.week_4, info.week_5, info.week_6, info.week_7, info.week_8]
    if request.method == 'GET':
        return render(request, 'points/email.html', {
            'week': week,
            'weeks': weeks,
        })
    else:
        username = request.user.username
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, 'points/email.html', {
                'week': week,
                'weeks': weeks,
                'message': 'Invalid password. Emails not sent.',
            })
        day = request.POST['week']
        day = datetime.strptime(day, '%Y-%m-%d').date()
        this_week = program.get_week('number', day)
        groups = Group.objects.filter(group_type='bunk')
        for group in groups:
            for camper in group.bunk_camper.all():
                rank = camper.rank
                sheets = MarkedSheet.objects.filter(camper=camper, date__lte=day)
                co_week = 0
                lt_week = 0
                ca_week = 0
                co_total = 0
                lt_total = 0
                ca_total = 0

                for sheet in sheets:
                    if sheet.name == 'bunk':
                        co_total += sheet.total
                        co_week += sheet.total if sheet.week ==this_week else 0
                    elif sheet.name == 'learning class':
                        lt_total += sheet.total
                        lt_week += sheet.total if sheet.week == this_week else 0
                    else:
                        ca_total += sheet.total
                        ca_week += sheet.total if sheet.week == this_week else 0
                    
                total = co_total + lt_total + ca_total
                week_total = co_week + lt_week + ca_week
                before = total - week_total
                before_rank = get_rank(before)
                c_id = f'{camper.id}x{camper.last_name[0]}'
                more = False
                if before_rank != rank:
                    more = f'Your son has been promoted from {before_rank} to {rank}!'

                message = f'{camper}. Rank: {rank}\n'
                if more:
                    message += f'{more}\n'
                message += f'Counselor points for this week: {co_week}\n Learning teacher points for this week: {lt_week}\n \n Total points: {total}\n'
                message += f'For a detailed breakdown of your son\'s points, please visit https://cgifth.herokuapp.com/profile/{c_id}'

                if camper.father_email != '' or camper.mother_email != '':
                    send_mail(
                        f'Tzivos Hashem Update, Week {week}',
                        message,
                        settings.EMAIL_HOST_USER,
                        [camper.father_email, camper.mother_email],
                        fail_silently=True
                    )
        return render(request, 'points/email.html', {
            'week': week,
            'weeks': weeks,
            'message': 'Emails sent.',
            })
