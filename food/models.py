from django.db import models
from manager.models import manager_account
from smart_restaurant.settings import TIME_ZONE
from django.utils import timezone

# Create your models here.
class food_item(models.Model):
    food_title = models.CharField(max_length=150)
    food_description = models.CharField(max_length=250,blank=True)
    food_price = models.FloatField()
    serving_quantity = models.IntegerField(default=1)
    image = models.ImageField(default='default.png', upload_to='images/')
    created_by = models.ForeignKey(manager_account, on_delete=models.CASCADE)
    date_of_creation = models.DateField(default=timezone.now)

    def __str__(self):
        return self.food_title