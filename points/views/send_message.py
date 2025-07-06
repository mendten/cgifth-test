from django.shortcuts import  HttpResponseRedirect #type: ignore
from django.contrib.auth.decorators import login_required #type: ignore
from django.urls import reverse #type: ignore

from points.models import User, Message #type: ignore


@login_required
def send_message(request):
    if request.method == 'POST':
        message = Message(sender=request.user)
        message.save()
        to = User.objects.filter(position='admin')
        message.to.add(*to)
        message.text = request.POST['message']
        message.save()
        return HttpResponseRedirect(reverse('index'))
