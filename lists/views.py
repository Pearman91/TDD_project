from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        context_dict = {'new_item_text': new_item_text}
        return redirect('/')

    context_dict = {'items': Item.objects.all()}
    return render(request, 'index.html', context=context_dict)
    # return render(request, 'index.html')
