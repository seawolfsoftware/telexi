from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Subscribers


@login_required
def subscribers(request):

    recipient_list = Subscribers.objects.all()

    return render(request, 'subscribe/subscribers.html',
                           {'recipient_list': recipient_list})


def confirm(request):

    sub = Subscribers.objects.get(email=request.GET['email'])

    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return render(request, 'subscribe/confirmed.html',
                               {'email': sub.email, 'action': 'confirmed'})
    else:
        return render(request, 'subscribe/denied.html',
                               {'email': sub.email, 'action': 'denied'})