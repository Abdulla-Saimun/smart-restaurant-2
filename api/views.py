from django.shortcuts import render
from .serializers import FoodMenuSerializer
from rest_framework import generics
from rest_framework import mixins
from .serializers import food_item


# Create your views here.
class FoodMenuList(generics.ListAPIView):
    queryset = food_item.objects.all()
    serializer_class = FoodMenuSerializer


class FoodDetailSingle(generics.RetrieveAPIView):
    queryset = food_item.objects.all()
    serializer_class = FoodMenuSerializer
