from rest_framework import serializers
from food.models import food_item


class FoodMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = food_item
        fields = '__all__'
