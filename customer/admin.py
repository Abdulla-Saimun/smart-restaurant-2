from django.contrib import admin
from django.contrib.auth.models import User
from .models import CartItems


# Register your models here.


class CartItemsAdmin(admin.ModelAdmin):
    '''fieldsets = [
        ("Order Status", {'fields': ["status"]}),
        ("Delivery Date", {'fields': ["delivery_date"]})

    ]'''
    list_display = ('id', 'user', 'item', 'quantity', 'ordered', 'ordered_date', 'delivery_date', 'status')
    list_filter = ('ordered', 'ordered_date', 'status')


admin.site.register(CartItems, CartItemsAdmin)
