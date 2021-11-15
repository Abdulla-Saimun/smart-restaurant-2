from django.db import models

# Create your models here.
class food(models.Model):
    category = models.CharField(max_length=254)
    title = models.CharField(max_length=100)
      
    