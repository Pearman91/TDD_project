import sys
import uuid

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from accounts.models import Token


def login(request):
    print('login_view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')


def send_login_email(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print(f'saving uid {uid} for email {email}', file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail('Log in to Superlists!',
              f'Link to log in: {url}',
              'noreply@superlists',
              [email],)
    return render(request, 'login_email_sent.html')

