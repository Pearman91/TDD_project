from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    return render(request, 'index.html')


def view_lists(request):
    items = Item.objects.all()
    return render(request, 'list.html', context={'items': items})


def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-list/')
