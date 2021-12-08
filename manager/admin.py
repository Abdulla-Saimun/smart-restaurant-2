from django.contrib import admin
from .models import manager_account, OrderList


class OrderlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product_id', 'total', 'products')

# Register your models here.


admin.site.register(manager_account)
admin.site.register(OrderList, OrderlistAdmin)
