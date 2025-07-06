from django.shortcuts import HttpResponseRedirect, render #type: ignore
from django.urls import reverse #type: ignore

from points.models import User, Group, Message #type: ignore
from points.wrappers import admin_only #type: ignore
      

@admin_only
def message(request):
    program = request.user.program
    if request.method == 'GET':
        bunks = Group.objects.filter(group_type='bunk', program=program).order_by('number')
        classes = Group.objects.filter(group_type='learning_class', program=program).order_by('number')
        messages = Message.objects.filter(to=request.user)
        return render(request, 'points/message.html', {
            'bunks': bunks,
            'classes': classes,
            'messages': messages,
        })
    else:
        if request.POST['action'] == 'send':
            # get which staff the message is for
            if request.POST['to'] == 'all':
                staff = User.objects.filter(position__in=['counselor', 'teacher'], program=program)
                message = Message.objects.get(sender=request.user, group='all')
            elif request.POST['to'] == 'counselors':
                staff = User.objects.filter(position='counselor', program=program)
                message = Message.objects.get(sender=request.user, group='counselors')
            elif request.POST['to'] == 'teachers':
                staff = User.objects.filter(position='teacher', program=program)
                message = Message.objects.get(sender=request.user, group='teachers')
            else:
                ids = request.POST.getlist('specific-staff')
                staff = User.objects.filter(pk__in=ids)
                message = Message(sender=request.user)
                message.save()
            for person in staff:
                if person not in message.to.all():
                    message.to.add(person)
            message.text = request.POST['content']
            message.save()

        elif request.POST['action'] == 'delete':
            message = Message.objects.get(pk=request.POST['message-id'])
            message.delete()

        return HttpResponseRedirect(reverse('message'))
