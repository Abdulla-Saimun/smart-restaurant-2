from django.shortcuts import render, redirect, get_object_or_404
# from .models import customer_account
# from .forms import customer_account_form, customer_login_form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import NewUSerForm
from food.models import food_item
from django.contrib.auth.hashers import check_password
from django.views.generic import (
    DetailView,
    DeleteView
)
from .models import CartItems
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.http import HttpResponseRedirect


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
    return render(request, 'customer/registration.html', {'signform': form, 'usr': 'Customer', 'login_var': 'Registration'})


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
    return render(request, 'customer/login.html', {'form': form, 'usr': 'Customer', 'login_var': 'Login'})


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


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(food_item, pk=pk)
    cart_item = CartItems.objects.create(
        item=item,
        user=request.user,
        ordered=False,
    )
    return HttpResponseRedirect(reverse('customer:cart'))

    #return reverse('customer:cart', kwargs={'pk': pk})


@login_required
def get_cart_items(request):
    cart_items = CartItems.objects.filter(user=request.user, ordered=False)
    total_item = cart_items.count()
    bill = cart_items.aggregate(Sum('item__food_price'))
    number = cart_items.aggregate(Sum('quantity'))
    print(number)
    print(bill)
    pieces = cart_items.aggregate(Sum('item__serving_quantity'))
    print(pieces)
    total = bill.get("item__food_price__sum")
    print(total)
    count = number.get("quantity__sum")
    total_pieces = pieces.get("item__serving_quantity__sum")
    context = {
        'cart_items': cart_items,
        'total': total,
        'count': count,
        'total_pieces': total_pieces,
        'total_item': total_item
    }
    return render(request, 'customer/cart.html', context)


class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItems
    success_url = '/cart'

    def test_func(self):
        cart = self.get_object()
        if self.request.user == cart.user:
            return True
        return False


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
