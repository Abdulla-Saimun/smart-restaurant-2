from django.shortcuts import render
from .forms import manager_account_form
# Create your views here.

def manager_registration(request):
    form = manager_account_form()
    context = {
        'regForm': form,
        'msgtype': 'failed',
        'message': ''
    }
    if request.method == 'POST':
        form = manager_account_form(request.POST, request.FILES)        
        if form.is_valid():
            form.save()
            context.update({
                'message': 'Registration is successful',
                'msgtype': 'successful'
            })
        else:
            context.update({
                'message': 'Try Again',
                'msgtype': 'failed'
            })
   
    return render(request, 'manager/signup.html', context)