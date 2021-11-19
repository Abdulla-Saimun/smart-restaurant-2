from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class manager_account(models.Model):
    man_userid = models.CharField(max_length=100, primary_key=True)
    man_fullname = models.CharField(max_length=100, blank=False, null=False)
    man_email = models.CharField(max_length=100, blank=False, null=False)
    man_pass = models.CharField(max_length=50, blank=False, null=False)
    man_phone = models.CharField(max_length=11, blank=False, null=False)

    def save(self, *args, **kwargs):
        self.man_pass = make_password(self.man_pass)
        super(manager_account, self).save(*args, **kwargs)

    def __str__(self):
        return '{} and {}'.format(self.man_fullname, self.man_userid)
    



class food(models.Model):
    category = models.CharField(max_length=254)
    title = models.CharField(max_length=100)
      
    
