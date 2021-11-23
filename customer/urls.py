from django.urls import path
from . import views
from food.views import menu_list

urlpatterns = [
   path('', views.customer_dashboard, name="customer_dashboard"),
   path('registration', views.registration, name='registration'),
   path('explore/', menu_list, name='explore'),
   path('login', views.login_customer, name='cus-login'),
   path('logout', views.logout_view, name='logout')
    
]