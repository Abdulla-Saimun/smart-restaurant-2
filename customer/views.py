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
from .models import CartItems, Customer_feedback
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from manager.models import OrderList


def customer_dashboard(request):
    feedback = Customer_feedback.objects.all().order_by('id').reverse()
    context = {
        'feedbacks': feedback
    }
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
    return render(request, 'customer/registration.html',
                  {'signform': form, 'usr': 'Customer', 'login_var': 'Registration'})


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
    messages.info(request, "Added to Cart Successfully!!Continue Shopping!!")
    return HttpResponseRedirect(reverse('customer:cart'))

    # return reverse('customer:cart', kwargs={'pk': pk})


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


@login_required
def order_food_by_customer(request):
    cart_items = CartItems.objects.filter(user=request.user, ordered=False)
    ordered_date = timezone.now()
    cart_items.update(ordered=True, ordered_date=ordered_date)
    messages.info(request, "Item Ordered")
    return redirect("customer:order_details")


@login_required
def order_details_by_customer(request):
    context = {}
    try:
        items_active = CartItems.objects.filter(user=request.user, ordered=True, status="Active").order_by(
            '-ordered_date')
        bill = items_active.aggregate(Sum('item__food_price'))
        number = items_active.aggregate(Sum('quantity'))
        pieces = items_active.aggregate(Sum('item__serving_quantity'))
        total = bill.get("item__food_price__sum")
        count = number.get("quantity__sum")
        total_pieces = pieces.get("item__serving_quantity__sum")
        product_list = []
        cart_id_list = []
        for i in items_active:
            product_list.append(i.item.food_title)
            cart_id_list.append(i.id)
        print(product_list)
        cust = str(request.user)
        if items_active:
            date = items_active[0].ordered_date
            print(date)

        date_now = timezone.now()
        order_check = OrderList.objects.filter(customer=cust, status='Active', date=date_now)
        print(order_check)
        print(type(order_check))
        if order_check:
            order_check.update(products=product_list, total=total, product_id=cart_id_list)
            print('if executed')
        else:
            orderCreate = OrderList.objects.create(products=product_list, customer=cust, date=timezone.now(),
                                                   total=total,
                                                   status='Active', product_id=cart_id_list)
            orderCreate.save()
            print('else executed')

        context = {
            'active': items_active,
            'deliver': '',
            'total': total,
            'count': count,
            'total_pieces': total_pieces,
            'process': ''
        }
    except:
        pass

    try:
        cart_items_delivered = CartItems.objects.filter(user=request.user, ordered=True, status="Delivered").order_by(
            '-ordered_date')
        context.update({'deliver': cart_items_delivered})
    except:
        pass

    try:
        cart_items_processed = CartItems.objects.filter(user=request.user, ordered=True, status="Processing").order_by(
            '-ordered_date')
        context.update({'process': cart_items_processed})
    except:
        pass
    return render(request, 'customer/order_detail.html', context)


def customer_feedback(request):
    if request.method == 'POST':
        contentbody = request.POST['textcontent']
        if contentbody:
            date = timezone.now()
            user = request.user
            feedback = Customer_feedback.objects.create(content=contentbody, date=date, customer=user)
            feedback.save()
        return HttpResponseRedirect(reverse('customer:customer_dashboard'))


def sort_by_pizza(request):
    try:
        pizzas = food_item.objects.filter(food_catagory='Pizza')
        context = {
            'items': pizzas
        }
        return render(request, 'customer/explorefood.html', context)
    except:
        return HttpResponseRedirect(reverse('customer:explore'))


def sort_by_burger(request):
    try:
        pizzas = food_item.objects.filter(food_catagory='Burger')
        context = {
            'items': pizzas
        }
        return render(request, 'customer/explorefood.html', context)
    except:
        return HttpResponseRedirect(reverse('customer:explore'))


def sort_by_chicken(request):
    try:
        pizzas = food_item.objects.filter(food_catagory='Chicken')
        context = {
            'items': pizzas
        }
        return render(request, 'customer/explorefood.html', context)
    except:
        return HttpResponseRedirect(reverse('customer:explore'))


def sort_by_drinks(request):
    try:
        pizzas = food_item.objects.filter(food_catagory='Drinks')
        context = {
            'items': pizzas
        }
        return render(request, 'customer/explorefood.html', context)
    except:
        return HttpResponseRedirect(reverse('customer:explore'))


def sort_by_sandwich(request):
    try:
        pizzas = food_item.objects.filter(food_catagory='Sandwich')
        context = {
            'items': pizzas
        }
        return render(request, 'customer/explorefood.html', context)
    except:
        return HttpResponseRedirect(reverse('customer:explore'))


def sort_by_fry(request):
    try:
        pizzas = food_item.objects.filter(food_catagory='Fry')
        context = {
            'items': pizzas
        }
        return render(request, 'customer/explorefood.html', context)
    except:
        return HttpResponseRedirect(reverse('customer:explore'))


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
