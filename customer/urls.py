from django.urls import path
from . import views

urlpatterns = [
   path('', views.customer_dashboard, name="customer_dashboard"),
   path('registration', views.registration, name='registration'),
   path('login', views.login_customer, name='cus-login'),
   path('logout', views.logout_view, name='logout')
    
]