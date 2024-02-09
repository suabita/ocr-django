from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from nutritional_table.models import NutritionalTable
from nutritional_table.forms import NutritionalTableForm
from django.urls import reverse_lazy

# Create your views here.

class NutritionalTableCreateView(LoginRequiredMixin, CreateView):
    model = NutritionalTable
    template_name = 'nutritional_table/form.html'
    form_class = NutritionalTableForm
    success_url = reverse_lazy('authentication:home') 

    def form_valid(self, form):
        # Antes de guardar el formulario, establecemos el valor del campo campo_a_setear
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        context['user'] = self.request.user
        print("user_context home", self.request.user)
        return context