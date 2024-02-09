from django.urls import path
from authentication.views import SignUpView, ProfileView, HomeView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

app_name = 'authentication'

urlpatterns = [
    path('signup/', SignUpView.as_view(),
             name='signup'),
    path('signup/done/', TemplateView.as_view(
            template_name='authentication/signup_done.html'),
             name='signup_done'),
    path('profile-update/<int:pk>/', ProfileView.as_view(), name='update'),
    path('home/', HomeView.as_view(),
             name='home'),
    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
]
