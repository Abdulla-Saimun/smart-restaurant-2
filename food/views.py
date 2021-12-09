from django.shortcuts import render, get_object_or_404
from .models import food_item
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    ListView,
    DeleteView
)
from django.urls import reverse
from .forms import FoodItemModelForm


# Create your views here.


class FoodDetailView(DetailView):
    template_name = 'food/food_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(food_item, id=id_)


class FoodUpdateView(UpdateView):
    template_name = 'food/food_create.html'
    form_class = FoodItemModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(food_item, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class FoodlistView(ListView):
    template_name = 'manager/food_list.html'
    queryset = food_item.objects.all()


class FoodCreateView(CreateView):
    template_name = 'food/food_create.html'
    form_class = FoodItemModelForm
    queryset = food_item.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class FoodDeleteView(DeleteView):
    template_name = 'food/food_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(food_item, id=id_)

    def get_success_url(self):
        return reverse('food:food-list')
