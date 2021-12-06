from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from food.models import food_item


class CartItems(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(food_item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
    delivery_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return self.item.food_title

    def get_remove_from_cart_url(self):
        return reverse("customer:remove-from-cart", kwargs={
            'pk': self.pk
        })

    def update_status_url(self):
        return reverse("customer:update_status", kwargs={
            'pk': self.pk
        })


'''
# Create your models here.
class customer_account(models.Model):
    select_gender = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    cus_userid = models.CharField(max_length=100, primary_key=True)
    cus_fullname = models.CharField(max_length=100, blank=False, null=False)
    cus_email = models.CharField(max_length=100, blank=False, null=False)
    cus_gender = models.CharField(choices=select_gender, blank=True, null=True, max_length=20)
    cus_pass = models.CharField(max_length=50, blank=False, null=False)
    cus_phone = models.CharField(max_length=11, blank=False, null=False)
    cus_address = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.cus_pass = make_password(self.cus_pass)
        super(customer_account, self).save(*args, **kwargs)

    def __str__(self):
        return self.cus_userid
'''
