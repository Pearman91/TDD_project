from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    context_dict = {'new_item_text': request.POST.get('item_text', '')}
    # if request.method == 'POST':
    return render(request, 'index.html', context=context_dict)
    # return render(request, 'index.html')
