from django.db import models

# Create your models here.
class customer_account(models.Model):
<<<<<<< HEAD
    select_gender = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    cus_userid = models.CharField(max_length=100, primary_key=True)
    cus_fullname = models.CharField(max_length=100, blank=False, null=False)
    cus_email = models.CharField(max_length=100, blank=False, null=False)
    cus_gender = models.CharField(choices=select_gender, blank=True, null=True, max_length=20)
=======
    cus_userid = models.CharField(max_length=100, primary_key=True)
    cus_fullname = models.CharField(max_length=100, blank=False, null=False)
    cus_email = models.CharField(max_length=100, blank=False, null=False)
>>>>>>> b858f5f84ea0c3b32b0e17ac3cb3d8bcf004551e
    cus_pass = models.CharField(max_length=50, blank=False, null=False)
    cus_phone = models.CharField(max_length=11, blank=False, null=False)
    cus_address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.cus_userid
    