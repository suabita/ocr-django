from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from nutrient.models import Nutrient
from nutrient.forms import NutrientForm
from django.urls import reverse_lazy

# Create your views here.

class NutrientCreateView(LoginRequiredMixin, CreateView):
    model = Nutrient
    template_name = 'nutrient/form.html'
    form_class = NutrientForm
    success_url = reverse_lazy('authentication:home') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        context['user'] = self.request.user
        print("user_context home", self.request.user)
        return context

class NutrientUpdateView(LoginRequiredMixin, UpdateView):
    model = Nutrient
    template_name = 'nutrient/form.html'
    form_class = NutrientForm
    success_url = reverse_lazy('authentication:home') 
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['action'] = 'Update'
        print("user_context home", self.request.user)
        return context


class NutrientListView(LoginRequiredMixin, ListView):
    model = Nutrient
    template_name = 'nutrient/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['action'] = 'List'
        print("user_context home", self.request.user)
        return context

