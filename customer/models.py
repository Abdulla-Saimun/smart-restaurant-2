'''from django.db import models
from django.contrib.auth.hashers import make_password


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