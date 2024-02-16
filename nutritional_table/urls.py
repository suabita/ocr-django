from django.urls import path
from nutritional_table.views import NutritionalTableCreateView, NutritionalTableListView, NutritionalTableUpdateView, NutritionalDetailView
from django.views.generic import TemplateView


app_name = 'nutritional_table'

urlpatterns = [
    path('create/', NutritionalTableCreateView.as_view(),
             name='create'),
    path('nutritional-update/<int:pk>/', NutritionalTableUpdateView.as_view(), name='update'),
    path('', NutritionalTableListView.as_view(),
             name='list'),
    path('detail/<int:pk>/', NutritionalDetailView.as_view(), name='detail'),
]
