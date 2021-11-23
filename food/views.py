from django.shortcuts import render
from .models import food_item
# Create your views here.

def menu_list(request):
    list_query = food_item.objects.all()
    print(list_query)
    context = {
        'items': list_query
    }
    return render(request, 'customer/explorefood.html', context)
