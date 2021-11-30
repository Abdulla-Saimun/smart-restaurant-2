from django.urls import path
from .import views

urlpatterns = [
    path('signup', views.manager_registration, name="signup"),
    path('login', views.manager_login, name='manager_login'),
    path('logout', views.manager_logout, name='manager_logout'),
    path('order', views.order_foods, name='order_foods'),
    path('overview', views.manager_overview, name='manager_overview')
]