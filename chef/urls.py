from django.urls import path
from . import views
from .views import FoodlistView

app_name = 'chef'
urlpatterns = [
    path('signup', views.chef_registration, name="chef-signup"),
    path('login', views.chef_login, name='chef_login'),
    path('logout', views.chef_logout, name='chef_logout'),
    path('order', views.chef_foods_order, name='chef_foods_order'),
    path('overview', views.chef_overview, name='chef_overview'),
    path('order-confirm/<int:id>', views.order_confirm, name='order-confirm'),
    path('all', views.all_order, name='all_order'),
    path('delivered', views.delivered_order, name='delivered'),
    path('active', views.active_order, name='active'),
    path('food-list', FoodlistView.as_view(), name='food_list')

]
'''def check():
    ses = request.session.has_key('chef_userid')
    if ses:
        pass
    else:
        return HttpResponseRedirect(reverse('chef:chef_login'))'''