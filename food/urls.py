from django.urls import path
from .views import FoodDetailView, FoodUpdateView, FoodlistView, FoodCreateView, FoodDeleteView


app_name = "food"
urlpatterns = [
    path('', FoodlistView.as_view(), name='food-list'),
    path('<int:id>/', FoodDetailView.as_view(), name='food-detail'),
    path('<int:id>/update/', FoodUpdateView.as_view(), name='food-update'),
    path('create/', FoodCreateView.as_view(), name='food-create'),
    path('<int:id>/delete/', FoodDeleteView.as_view(), name='food-delete')
]