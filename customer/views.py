from django.shortcuts import render

def customer_dashboard(request):
    context = {}
    return render(request, 'customer/dashboard.html', context)
 