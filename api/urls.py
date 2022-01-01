from django.urls import path
from .views import FoodMenuList, FoodDetailSingle

app_name = 'api'
urlpatterns = [
    path('food-list', FoodMenuList.as_view(), name='food-list'),
    path('food-details/<str:pk>', FoodDetailSingle.as_view(), name='food-detail'),
]
