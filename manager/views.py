from django.shortcuts import render, redirect
from .forms import manager_account_form, manager_login_raw_form
from .models import manager_account
from django.contrib.auth.hashers import check_password
from food.models import food_item
from customer.models import CartItems
from .models import OrderList
from django.urls import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from customer.models import Customer_feedback
from django.views import View

# reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table

# html to pdf
from io import StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from fpdf import FPDF
#
from django_xhtml2pdf.utils import generate_pdf


# from cgi import escape
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
                ses = request.session['man_userid']

                # return render(request, 'manager/manager_dashboard.html', context)
                return HttpResponseRedirect(reverse('manager:manager_overview'))
            else:
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

    return HttpResponseRedirect(reverse('manager:manager_login'))


def order_foods(request):
    ses = request.session.has_key('man_userid')
    if ses:
        try:
            queryset = OrderList.objects.filter(status='Active').order_by('id')
            context = {
                'orders': queryset
            }
            return render(request, 'manager/order.html', context)
        except:
            return render(request, 'manager/order.html')

    else:
        return HttpResponseRedirect(reverse('manager:manager_login'))


def processing_order(request):
    ses = request.session.has_key('man_userid')
    if ses:
        try:
            queryset = OrderList.objects.filter(status='Processing').order_by('id').reverse()
            context = {
                'orders': queryset
            }
            return render(request, 'manager/processing_order.html', context)
        except:
            return render(request, 'manager/processing_order.html')

    else:
        return HttpResponseRedirect(reverse('manager:manager_login'))


def delivered_order(request):
    ses = request.session.has_key('man_userid')
    if ses:
        try:
            queryset = OrderList.objects.filter(status='Delivered').order_by('id').reverse()
            context = {
                'orders': queryset
            }
            return render(request, 'manager/delivered_order.html', context)
        except:
            return render(request, 'manager/delivered_order.html')

    else:
        return HttpResponseRedirect(reverse('manager:manager_login'))


def all_order(request):
    ses = request.session.has_key('man_userid')
    if ses:
        try:
            queryset = OrderList.objects.all().order_by('id').reverse()
            context = {
                'orders': queryset
            }
            return render(request, 'manager/all_order.html', context)
        except:
            return render(request, 'manager/all_order.html')

    else:
        return HttpResponseRedirect(reverse('manager:manager_login'))


def manager_overview(request):
    ses = request.session.has_key('man_userid')
    if ses:
        try:
            query_quantity = food_item.objects.all().count()
            total_amouont = OrderList.objects.filter(status='Processing')
            active_order = OrderList.objects.filter(status='Active').count()
            in_process = total_amouont.count()
            x = total_amouont.aggregate(Sum('total'))
            total_process = x.get('total__sum')
            t_del = OrderList.objects.filter(status='Delivered')
            y = t_del.aggregate(Sum('total'))
            total_delivered = y.get('total__sum')
            total = total_process + total_delivered
            print(total)
            context = {
                'total_item': query_quantity,
                'total_amount': total,
                'active_order': active_order,
                'in_process': in_process
            }
            return render(request, 'manager/manager_dashboard.html', context)
        except:
            pass

    else:
        return HttpResponseRedirect(reverse('manager:manager_login'))


def order_confirm(request, id):
    ses = request.session.has_key('man_userid')
    if ses:
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

        return HttpResponseRedirect(reverse('manager:order_foods'))
    else:
        return HttpResponseRedirect(reverse('manager:manager_login'))


def feedback_view(request):
    ses = request.session.has_key('man_userid')
    if ses:
        feed = Customer_feedback.objects.all().order_by('id').reverse()
        context = {
            'feedbacks': feed
        }
        return render(request, 'manager/feedback.html', context)
    else:
        return HttpResponseRedirect(reverse('manager:manager_login'))


def delete_order(request, id):
    ses = request.session.has_key('man_userid')
    if ses:
        get_order = OrderList.objects.get(id=id)
        get_cart_ids = get_order.product_id
        print(get_cart_ids)
        for i in get_cart_ids:
            x = int(i)
            print(x)
            cartid = CartItems.objects.get(id=x)
            if cartid:
                cartid.delete()
        x = OrderList.objects.get(id=id)
        x.delete()
        return HttpResponseRedirect(reverse('manager:order_foods'))
    else:
        return HttpResponseRedirect(reverse('manager:manager_login'))


def delete_feedback(request, id):
    ses = request.session.has_key('man_userid')
    if ses:
        try:
            getFeed = Customer_feedback.objects.get(id=id)
            getFeed.delete()
        except:
            return HttpResponseRedirect(reverse('manager:feedback'))
        return HttpResponseRedirect(reverse('manager:feedback'))
    else:
        return HttpResponseRedirect(reverse('manager:manager_login'))


def report_page(request):
    x = OrderList.objects.all()
    dateList = []
    for i in x:
        dateList.append(i.date)

    dateList = list(dict.fromkeys(dateList))
    dateList.sort(reverse=True)
    context = {
        'dates': dateList
    }
    return render(request, 'manager/reporthome.html', context)


def search_report(request):
    if request.method == 'POST':
        txt = request.POST['date']
        monthDictionary = {
            'Jan': "01",
            'Feb': "02",
            'Mar': "03",
            'Apr': "04",
            'May': "05",
            'Jum': "06",
            'Jul': "07",
            'Aug': "08",
            'Sep': "09",
            'Oct': "10",
            'Nov': "11",
            'Dec': "12"
        }
        "YYYY-MM-DD"
        x = txt.split(", ")
        first = x[0]
        year = x[1]
        firtsSplit = first.split(". ")
        month = monthDictionary[firtsSplit[0]]
        day = firtsSplit[1]
        dateValue = year + '-' + month + '-' + day
        print(dateValue)
        print('saimun')
        filterbydate = OrderList.objects.filter(date=str(dateValue))
        print(filterbydate.count())
        if filterbydate:
            print(filterbydate)
        else:
            print('no item found')
    return render(request, 'manager/reporthome.html')


def generate_report_by_reportLab(request):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textobj = c.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont('Helvetica', 14)
    lines = [
        'this is line one',
        'this is  line  two',
        'this is line three'
    ]
    for line in lines:
        textobj.textLine(line)

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='report.pdf')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def view_report(request):
    if request.method == 'POST':
        txt = request.POST['date']
        monthDictionary = {
            'Jan': "01",
            'Feb': "02",
            'Mar': "03",
            'Apr': "04",
            'May': "05",
            'Jum': "06",
            'Jul': "07",
            'Aug': "08",
            'Sep': "09",
            'Oct': "10",
            'Nov': "11",
            'Dec': "12"
        }
        x = txt.split(", ")
        first = x[0]
        year = x[1]
        firtsSplit = first.split(". ")
        month = monthDictionary[firtsSplit[0]]
        day = firtsSplit[1]
        dateValue = year + '-' + month + '-' + day
        print(dateValue)
        filterbydate = OrderList.objects.filter(date=dateValue)
        tt = filterbydate.aggregate(Sum('total'))
        grand_total = tt.get('total__sum')
        print(tt)
        context = {
            'reports': filterbydate,
            'dte': txt,
            'total': grand_total,
        }
        pdf = render_to_pdf('manager/manager_pdf_template.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

    return HttpResponseRedirect(reverse('manager:report-home'))


def generate_reportbyhtml(request):
    results = OrderList.objects.all()

    resdict = dict({
        'pagesize': 'A4',
        'mylist': results,
    })
    return render_to_pdf(
        'manager/manager_pdf_template.html',
        resdict
    )


def pdf_check(request):
    main_list = list()
    filterdate = OrderList.objects.filter(date='2021-12-8')
    if filterdate:
        for date in filterdate:
            nsdict = dict()
            nsdict['id'] = str(date.id)
            nsdict['products'] = date.products
            nsdict['customer'] = date.customer
            nsdict['date'] = date.date
            nsdict['total'] = date.total
            main_list.append(nsdict)
        print(main_list)
    sales = [
        {"item": "Keyboard", "amount": "$120,00"},
        {"item": "Mouse", "amount": "$10,00"},
        {"item": "House", "amount": "$1 000 000,00"},
    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Report:', 0, 1)
    pdf.cell(40, 10, '', 0, 1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8,
             f"{'Id'.ljust(5)} {'Product'.rjust(10)} {'Customer'.rjust(20)}{'date'.rjust(10)}{'total'.rjust(10)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in main_list:
        pdf.cell(200, 8, f"{line['id'].ljust(5)} {line['products']} {line['customer']} {line['date']} {line['total']}",
                 0, 1)
    pdf.output('report.pdf', 'F')
    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')


'''
def pdf_check(response):
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('manager/manager_pdf_template.html', file_object=resp)
    return result '''

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
