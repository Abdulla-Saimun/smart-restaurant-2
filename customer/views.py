from django.shortcuts import render, redirect, get_object_or_404
# from .models import customer_account
# from .forms import customer_account_form, customer_login_form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import NewUSerForm
from food.models import food_item
from django.contrib.auth.hashers import check_password
from django.views.generic import (
DetailView
)


def customer_dashboard(request):
    context = {}
    return render(request, 'customer/cushome.html', context)


def registration(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        context = {
            'signform': form,
            'message': '',
            'msgtype': 'failed'

        }
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = NewUSerForm()
    return render(request, 'customer/registration.html', {'signform': form})


# login
def login_customer(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'customer/login.html', {'form': form})


# logout
def logout_view(request):
    logout(request)
    return redirect('/')


def explore(request):
    return render(request, 'customer/explorefood.html', {})


# return redirect('/')

def menu_list(request):
    list_query = food_item.objects.all()
    print(list_query)
    context = {
        'items': list_query
    }
    return render(request, 'customer/explorefood.html', context)


class CusFoodDetailView(DetailView):
    template_name = 'customer/customer_foodview.html'

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('id')
        return get_object_or_404(food_item, id=id_)


'''def registration(request):
    form = customer_account_form()
    context = {
        'frms': form,
        'msgtype': 'failed',
        'message': ''
    }
    if request.method == 'POST':
        form = customer_account_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = customer_account_form()
            context.update({
                'message': 'Registration is successful',
                'msgtype': 'successful'
            })
        else:
            context.update({
                'message': 'Try Again',
                'msgtype': 'failed'
            })

    return render(request, 'customer/registration.html', context)


#def login(request):
   # if request.session.has_key('cus_userid'):
     #   return redirect('../')
  #  else:
   #     context = {'loginForm': customer_login_form()}
    #    if request.method == 'POST':
     #       form = customer_account_form(request.POST)
      ###        request.session['cus_userid'] = form.data['cus_userid']
         #       return redirect('../')
          #  else:
           #     context.update({'message': 'Invalid credential!'})
      #  return render(request, 'customer/login.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        pc = customer_account.objects.get(cus_userid=username)
        if pc is not None:
            z = pc.cus_pass
            cp = check_password(password, z)
            if cp:
                user = customer_account.objects.filter(cus_userid=username)
            if user is not None:
                request.session['cus_userid'] = username
                return redirect('/')
            else:
                messages.info(request, 'invalid credential')
                return redirect('login')

    return render(request, 'customer/login.html')


def logout(request):
    try:
        del request.session['cus_userid']
    except KeyError:
        pass
    return redirect('/')
'''
