from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class chef_account(models.Model):
    chef_userid = models.CharField(max_length=100, primary_key=True)
    chef_fullname = models.CharField(max_length=100, blank=False, null=False)
    chef_email = models.CharField(max_length=100, blank=False, null=False)
    chef_pass = models.CharField(max_length=10000, blank=False, null=False)
    chef_phone = models.CharField(max_length=11, blank=False, null=False)

    def save(self, *args, **kwargs):
        self.man_pass = make_password(self.chef_pass)
        super(chef_account, self).save(*args, **kwargs)

    def __str__(self):
        return 'id: {}'.format(self.chef_userid)


