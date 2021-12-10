from django.urls import path
from .import views


app_name = 'manager'
urlpatterns = [
    path('signup', views.manager_registration, name="signup"),
    path('login', views.manager_login, name='manager_login'),
    path('logout', views.manager_logout, name='manager_logout'),
    path('order', views.order_foods, name='order_foods'),
    path('overview', views.manager_overview, name='manager_overview'),
    path('order-confirm/<int:id>', views.order_confirm, name='order-confirm'),
    path('processing', views.processing_order, name='processing'),
    path('delivered', views.delivered_order, name='delivered'),
    path('all', views.all_order, name='all_order'),
    path('feedback', views.feedback_view, name='feedback')

]
