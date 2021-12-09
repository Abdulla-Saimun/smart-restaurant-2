from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class manager_account(models.Model):
    man_userid = models.CharField(max_length=100, primary_key=True)
    man_fullname = models.CharField(max_length=100, blank=False, null=False)
    man_email = models.CharField(max_length=100, blank=False, null=False)
    man_pass = models.CharField(max_length=10000, blank=False, null=False)
    man_phone = models.CharField(max_length=11, blank=False, null=False)

    def save(self, *args, **kwargs):
        self.man_pass = make_password(self.man_pass)
        super(manager_account, self).save(*args, **kwargs)

    def __str__(self):
        return 'id: {}'.format(self.man_userid)


class food(models.Model):
    category = models.CharField(max_length=254)
    title = models.CharField(max_length=100)


class OrderList(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered')
    )
    products = ArrayField(models.CharField(max_length=500), blank=True)
    customer = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
    total = models.FloatField()
    product_id = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('manager:order-confirm', kwargs={'id': self.id})

    def get_absolute_url_chef(self):
        return reverse('chef:order-confirm', kwargs={'id': self.id})
