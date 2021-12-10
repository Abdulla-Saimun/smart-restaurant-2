from django.shortcuts import render, redirect
from django.urls import reverse
from .models import chef_account
from .forms import chef_account_form
from manager.models import OrderList
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from food.models import food_item
from customer.models import CartItems
from django.views.generic import ListView
from django.http import HttpResponseRedirect


# Create your views here.

def chef_registration(request):
    form = chef_account_form()
    context = {
        'regForm': form,
        'msgtype': 'failed',
        'message': ''
    }
    if request.method == 'POST':
        form = chef_account_form(request.POST, request.FILES)
        if form.is_valid():
            # user = form.cleaned_data.get('man_userid')
            password1 = form.data['chef_pass']
            password2 = request.POST['chef_pass2']
            if password1 == password2:
                form.save()
                form = chef_account_form()
                context.update({
                    'message': 'Registration is successful',
                    'msgtype': 'successful'
                })
            else:
                form = chef_account_form()
                context.update({
                    'message': ',Password Must be same',
                    'msgtype': 'failed'
                })

        else:
            context.update({
                'message': 'Try Again',
                'msgtype': 'failed'
            })

    return render(request, 'chef/signup.html', context)


def chef_login(request):
    if request.method == "POST":
        user_id = request.POST['signin-user']
        user_password = request.POST['signin-password']
        login_id = chef_account.objects.filter(chef_userid=user_id, chef_pass=user_password)
        if login_id:
            request.session['chef_userid'] = user_id
            orders = OrderList.objects.filter(status='Processing')
            total_item = food_item.objects.all().count()
            active_count = OrderList.objects.filter(status='Active').count()
            in_process = orders.count()
            total_delivered = OrderList.objects.filter(status='Delivered').count()
            context = {
                'orders': orders,
                'total_item': total_item,
                'active_order': active_count,
                'in_process': in_process,
                'total_delivered': total_delivered
            }
            print('login successful')
            return render(request, 'chef/chef_dashboard.html', context)
        else:
            messages.success(request, "Invalid credential! Try again..")
            print('login failed')
            context = {
                'msg': 'failed and try again'
            }
            return render(request, 'chef/login.html', context)

    elif request.session.has_key('chef_userid'):
        print('already has a key')
        orders = OrderList.objects.filter(status='Processing')
        total_item = food_item.objects.all().count()
        active_count = OrderList.objects.filter(status='Active').count()
        in_process = orders.count()
        total_delivered = OrderList.objects.filter(status='Delivered').count()
        context = {
            'foods': orders,
            'total_item': total_item,
            'active_order': active_count,
            'in_process': in_process,
            'total_delivered': total_delivered
        }
        return render(request, 'chef/chef_dashboard.html', context)
    else:
        context = {
            'msg': 'Error credentials and try again'
        }
        return render(request, 'chef/login.html', context)


def chef_logout(request):
    if request.session.has_key('chef_userid'):
        print('key is deleted')
        del request.session['chef_userid']

    return HttpResponseRedirect(reverse('chef:chef_login'))


def chef_foods_order(request):
    ses = request.session.has_key('chef_userid')
    if ses:
        queryset = OrderList.objects.filter(status='Processing').order_by('id')
        context = {
            'orders': queryset
        }
        return render(request, 'chef/order.html', context)
    else:
        return HttpResponseRedirect(reverse('chef:chef_login'))


def active_order(request):
    ses = request.session.has_key('chef_userid')
    if ses:
        queryset = OrderList.objects.filter(status='Active').order_by('id')
        context = {
            'orders': queryset
        }
        return render(request, 'chef/active_order.html', context)
    else:
        return HttpResponseRedirect(reverse('chef:chef_login'))


def delivered_order(request):
    ses = request.session.has_key('chef_userid')
    if ses:
        queryset = OrderList.objects.filter(status='Delivered').order_by('id')
        context = {
            'orders': queryset
        }
        return render(request, 'chef/delivered_order.html', context)
    else:
        return HttpResponseRedirect(reverse('chef:chef_login'))


def all_order(request):
    ses = request.session.has_key('chef_userid')
    if ses:
        queryset = OrderList.objects.all().order_by('id')
        context = {
            'orders': queryset
        }
        return render(request, 'chef/all_order.html', context)
    else:
        return HttpResponseRedirect(reverse('chef:chef_login'))


def chef_overview(request):
    ses = request.session.has_key('chef_userid')
    if ses:
        orders = OrderList.objects.filter(status='Processing')
        total_item = food_item.objects.all().count()
        active_count = OrderList.objects.filter(status='Active').count()
        in_process = orders.count()
        total_delivered = OrderList.objects.filter(status='Delivered').count()

        context = {
            'orders': orders,
            'total_item': total_item,
            'active_order': active_count,
            'in_process': in_process,
            'total_delivered': total_delivered
        }
        return render(request, 'chef/chef_dashboard.html', context)
    else:
        return HttpResponseRedirect(reverse('chef:chef_login'))


def order_confirm(request, id):
    ses = request.session.has_key('chef_userid')
    if ses:
        order_check = OrderList.objects.get(id=id)
        get_id = order_check.product_id
        for i in get_id:
            x = int(i)
            c_item = CartItems.objects.filter(id=x, status='Processing')
            c_item.update(status='Delivered')

        order_status = OrderList.objects.filter(id=id, status='Processing')
        print(get_id)
        if order_status:
            order_status.update(status='Delivered')

        return HttpResponseRedirect(reverse('chef:chef_foods_order'))
    else:
        return HttpResponseRedirect(reverse('chef:chef_login'))


class FoodlistView(ListView):
    template_name = 'chef/food_list.html'
    queryset = food_item.objects.all()
