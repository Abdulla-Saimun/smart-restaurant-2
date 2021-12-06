from django.contrib import admin
from .models import food_item
# Register your models here.


class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'food_title', 'food_description', 'food_price', 'food_catagory', 'serving_quantity', 'created_by', 'date_of_creation')


admin.site.register(food_item, FoodItemAdmin)