from django.urls import path
from . import views
from .views import menu_list, CusFoodDetailView
from .views import registration, CartDeleteView

app_name = 'customer'
urlpatterns = [
    path('', views.customer_dashboard, name="customer_dashboard"),
    path('registration/', registration, name='customer_registration'),
    path('explore/', menu_list, name='explore'),
    path('login', views.login_customer, name='customer_login'),
    path('logout', views.logout_view, name='logout'),
    path('detail/<int:id>/', CusFoodDetailView.as_view(), name='cus-food-detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.get_cart_items, name='cart'),
    path('remove-from-cart/<int:pk>/', CartDeleteView.as_view(), name='remove-from-cart'),
    path('ordered/', views.order_food_by_customer, name='order_food'),
    path('order-detail/', views.order_details_by_customer, name='order_details'),
    path('feedback', views.customer_feedback, name='feedback'),
    path('pizza', views.sort_by_pizza, name='pizza'),
    path('burger', views.sort_by_burger, name='burger'),
    path('chicken', views.sort_by_chicken, name='chicken'),
    path('drinks', views.sort_by_drinks, name='drinks'),
    path('sandwich', views.sort_by_sandwich, name='sandwich'),
    path('fry', views.sort_by_fry, name='fry'),

]
