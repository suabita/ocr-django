from django.shortcuts import render
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LogoutView, LoginView
from authentication.forms import SignUpForm, ProfileForm
from django.urls import reverse_lazy
from authentication.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(CreateView):
    template_name = 'authentication/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('authentication:signup_done')


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'authentication/profile_form.html'
    form_class = ProfileForm
    model = User
    success_url = reverse_lazy('nutritional_table:list')  


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        print("user_context home", self.request.user)
        return context
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('authentication:login')    # Especifica la página a la que se redirigirá después del cierre de sesión


class CustomLoginView(LoginView):
    template_name='authentication/login.html'

    def form_invalid(self, form):
        # Agregar un mensaje de error
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context