from django.db import models
from manager.models import manager_account
from smart_restaurant.settings import TIME_ZONE
from django.utils import timezone


# Create your models here.
class food_item(models.Model):
    food_cate = [
        ('Pizza', 'Pizza'),
        ('Burger', 'Burger'),
        ('Chicken', 'Chicken'),
        ('Drinks', 'Drinks'),
        ('Sandwich', 'Sandwich'),
        ('Cake', 'Cake'),
        ('Donut', 'Donut'),
        ('Fry', 'Fry')
    ]
    food_title = models.CharField(max_length=150)
    food_description = models.CharField(max_length=250, blank=True)
    food_price = models.FloatField()
    food_catagory = models.CharField(choices=food_cate, blank=False, null=False, max_length=50)
    serving_quantity = models.IntegerField(default=1)
    image = models.ImageField(default='default.jpg', upload_to='images/')
    created_by = models.ForeignKey(manager_account, on_delete=models.CASCADE)
    date_of_creation = models.DateField(default=timezone.now)

    def __str__(self):
        return self.food_title
