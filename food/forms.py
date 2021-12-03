from django import forms

from .models import food_item


class FoodItemModelForm(forms.ModelForm):

    class Meta:
        model = food_item
        fields = [
            'food_title',
            'food_description',
            'food_price',
            'food_catagory',
            'serving_quantity',
            'image',
            'created_by',
            'date_of_creation'
        ]

