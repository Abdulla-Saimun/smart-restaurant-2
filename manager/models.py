from django.db import models

# Create your models here.

class manager_account(models.Model):
    man_userid = models.CharField(max_length=100, primary_key=True)
    man_fullname = models.CharField(max_length=100, blank=False, null=False)
    man_email = models.CharField(max_length=100, blank=False, null=False)
    man_pass = models.CharField(max_length=50, blank=False, null=False)
    man_phone = models.CharField(max_length=11, blank=False, null=False)

    def __str__(self):
<<<<<<< HEAD
        return '{} and {}'.format(self.man_fullname, self.man_userid)
=======
        return '{} and {}'.format(self.man_userid, self.man_phone)
>>>>>>> b858f5f84ea0c3b32b0e17ac3cb3d8bcf004551e
    



class food(models.Model):
    category = models.CharField(max_length=254)
    title = models.CharField(max_length=100)
      
    