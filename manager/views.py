from django.shortcuts import render, redirect
from .forms import manager_account_form, manager_login_raw_form
from .models import manager_account
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from food.models import food_item


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
    return render(request, 'manager/order.html')

def manager_overview(request):
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
