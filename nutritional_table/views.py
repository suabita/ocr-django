from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from nutritional_table.models import NutritionalTable
from nutritional_table.forms import NutritionalTableForm
from django.urls import reverse_lazy
from authentication.models import User
from django.views.generic import DetailView
from django.urls import reverse
from processing.process_main import ProcessingMain
from processing.async_processing import async_process_data

# Create your views here.

class NutritionalTableCreateView(LoginRequiredMixin, CreateView):
    model = NutritionalTable
    template_name = 'nutritional_table/form.html'
    form_class = NutritionalTableForm
    success_url = reverse_lazy('nutritional_table:list') 

    def form_valid(self, form):
        # Antes de guardar el formulario, establecemos el valor del campo campo_a_setear
        form.instance.user = self.request.user
        response = super().form_valid(form)
        #llamaria clase de procesamiento a traves de una funcion asincrona de zappa (decorador task)como en el receptor
        
        # ProcessingMain(self.request.user, self.object).run()
        async_process_data(self.request.user.id, self.object.pk, False)
        return response

    def get_success_url(self):
        return reverse('nutritional_table:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        context['user'] = self.request.user
        print("user_context home", self.request.user)
        return context
    

class NutritionalTableListView(LoginRequiredMixin, ListView):
    model = NutritionalTable
    template_name = 'nutritional_table/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("NutritionalTableListView",self.request.__dict__)
        context['user'] = self.request.user
        context['action'] = 'List'
        context['profile'] = User.objects.filter(username=self.request.user.username).last()
        print("user_context home", self.request.user)
        return context

    def get_queryset(self):
        # Obtén el usuario actualmente autenticado
        user = self.request.user

        # Filtra los objetos del modelo basado en el usuario actual
        queryset = super().get_queryset().filter(user=user)

        return queryset
    

class NutritionalTableUpdateView(LoginRequiredMixin, UpdateView):
    model = NutritionalTable
    template_name = 'nutritional_table/form.html'
    form_class = NutritionalTableForm
    success_url = reverse_lazy('nutritional_table:list') 

    def form_valid(self, form):
        # Antes de guardar el formulario, establecemos el valor del campo campo_a_setear
        form.instance.user = self.request.user
        response = super().form_valid(form)
        #llamaria clase de procesamiento a traves de una funcion asincrona de zappa (decorador task)como en el receptor
        
        # ProcessingMain(self.request.user, self.object).run()
        async_process_data(self.request.user.id, self.object.pk, False)
        return response
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['action'] = 'Update'
        context['profile'] = User.objects.filter(username=self.request.user.username).last()

        print("user_context home", self.request.user)
        return context



class NutritionalDetailView(LoginRequiredMixin, DetailView):
    model = NutritionalTable
    template_name = 'nutritional_table/detail.html'  # Nombre de tu plantilla de detalle

    def get_queryset(self):
        self.queryset = self.model.objects.filter(user=self.request.user).select_related('user')
        return super(NutritionalDetailView, self).get_queryset()
    
    def get(self, request, *args, **kwargs):
        
        if request.GET.get('custom_function') == 'true':
            # Ejecutar tu función personalizada aquí
            self.object = self.get_object()
            async_process_data(self.request.user.id, self.object.pk, True)
            context = self.get_context_data(object=self.object)
            print("CUSTOM FUNCTION",request.GET.get('custom_function'))
            return self.render_to_response(context)
        else:
            response = super().get(request, *args, **kwargs)
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['action'] = 'Update'
        context['profile'] = User.objects.filter(username=self.request.user.username).last()
        context['custom_function_url'] = f"{self.request.path}?custom_function=true"
        print("user_context home", self.request.user)
        return context
    

class NutritionalTableDeleteView(DeleteView):
    model = NutritionalTable
    success_url = reverse_lazy('nutritional_table:list')
    template_name = 'nutritional_table/delete_confirmation.html'