from django.contrib import admin
from .models import manager_account, OrderList
# Register your models here.
admin.site.register(manager_account)
admin.site.register(OrderList)
