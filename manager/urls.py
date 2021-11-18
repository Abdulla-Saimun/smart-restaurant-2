from django.urls import path
from .import views

urlpatterns = [
    path('mansignup', views.manager_registration, name="mansignup")
]