from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib import auth, messages
from django.shortcuts import render, redirect

from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid))
    send_mail('Hi, you can log in to Superlists',
              f'Link to log in: {url}',
              'noreply@superlists',
              [email],)
    messages.success(request, 'Check out your email for message with a link '
                              'to log in there!')
    return redirect('/')


def login(request):
    user = auth.authenticate(request.GET.get('token'))
    if user is not None:
        auth.login(request, user)
    return redirect('/')

