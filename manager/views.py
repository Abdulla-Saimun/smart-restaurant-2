from django.shortcuts import render, redirect
from .forms import manager_account_form, manager_login_raw_form
from .models import manager_account
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from food.models import food_item
from customer.models import CartItems
from .models import OrderList
from django.urls import reverse
from django.db.models import Sum


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
            # user = form.cleaned_data.get('man_userid')
            password1 = form.data['man_pass']
            password2 = request.POST['man_pass2']
            if password1 == password2:
                form.save()
                form = manager_account_form()
                context.update({
                    'message': 'Registration is successful',
                    'msgtype': 'successful'
                })
            else:
                form = manager_account_form()
                context.update({
                    'message': ',Password Must be same',
                    'msgtype': 'failed'
                })
            # formuser = form.data['man_userid']
            # print(formuser)
            # print(user)

        else:
            context.update({
                'message': 'Try Again',
                'msgtype': 'failed'
            })

    return render(request, 'manager/signup.html', context)


def manager_login(request):
    if request.method == "POST":
        user_id = request.POST['signin-user']
        user_password = request.POST['signin-password']
        login_id = manager_account.objects.filter(man_userid=user_id)
        if login_id:
            is_login_id = manager_account.objects.get(man_userid=user_id)
            login_pass = is_login_id.man_pass
            check_hash = check_password(user_password, login_pass)
            if check_hash:
                request.session['man_userid'] = user_id
                food_all = food_item.objects.all()
                context = {
                    'foods': food_all
                }
                print('login successful')
                return render(request, 'manager/manager_dashboard.html', context)
            else:
                messages.success(request, "Invalid credential! Try again..")
                print('login failed')
                context = {
                    'msg': 'failed and try again'
                }
                return render(request, 'manager/login.html', context)
    elif request.session.has_key('man_userid'):
        print('already has a keyy')
        food_all = food_item.objects.all()
        context = {
            'foods': food_all
        }
        return render(request, 'manager/manager_dashboard.html', context)
    else:
        context = {
            'msg': 'failed and try again'
        }
        return render(request, 'manager/login.html', context)


def manager_logout(request):
    if request.session.has_key('man_userid'):
        print('key is deleted')
        del request.session['man_userid']

    return render(request, 'manager/login.html')


def order_foods(request):
    queryset = OrderList.objects.filter(status='Active')
    context = {
        'orders': queryset
    }
    return render(request, 'manager/order.html', context)


def processing_order(request):
    queryset = OrderList.objects.filter(status='Processing')
    context = {
        'orders': queryset
    }
    return render(request, 'manager/processing_order.html', context)


def delivered_order(request):
    queryset = OrderList.objects.filter(status='Delivered')
    context = {
        'orders': queryset
    }
    return render(request, 'manager/delivered_order.html', context)


def all_order(request):
    queryset = OrderList.objects.all()
    context = {
        'orders': queryset
    }
    return render(request, 'manager/all_order.html', context)


def manager_overview(request):
    query_quantity = food_item.objects.all().count()
    total_amouont = OrderList.objects.filter(status='Processing')
    active_order = OrderList.objects.filter(status='Active').count()
    in_process = total_amouont.count()
    x = total_amouont.aggregate(Sum('total'))
    total = x.get('total__sum')
    print(total)
    context = {
        'total_item': query_quantity,
        'total_amount': total,
        'active_order': active_order,
        'in_process': in_process
    }
    return render(request, 'manager/manager_dashboard.html', context)


def order_confirm(request, id):
    order_check = OrderList.objects.get(id=id)
    get_id = order_check.product_id
    for i in get_id:
        x = int(i)
        c_item = CartItems.objects.filter(id=x, status='Active')
        c_item.update(status='Processing')

    order_status = OrderList.objects.filter(id=id, status='Active')
    print(get_id)
    if order_status:
        order_status.update(status='Processing')

    return render(request, 'manager/manager_dashboard.html')


'''def manager_login(request):
    if request.POST:
        user_id = request.POST['signin-user']
        user_password = request.POST['signin-password']
        try:
            user_check = manager_account.objects.get(man_userid=user_id)
            if user_check is not None:
                database_pass = user_check.man_pass
                print(database_pass)
                authenti = check_password(user_password, database_pass)
                if authenti:
                    usr = manager_account.objects.filter(man_userid=user_id)
                    print('it is ok')
                    request.session['man_userid'] = user_id
                    return render(request, 'manager/manager_dashboard.html')

        except:
            print('this is exceptional')
            return render(request, 'manager/login.html')

    context = {
        'login_var': 'Log in'
    }
    return render(request, 'manager/login.html', context)
'''
