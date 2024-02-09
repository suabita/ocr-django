from django.urls import path
from nutrient.views import NutrientCreateView, NutrientUpdateView, NutrientListView
from django.views.generic import TemplateView


app_name = 'nutrient'

urlpatterns = [
    path('create/', NutrientCreateView.as_view(),
             name='create'),
    path('update/<slug>/', NutrientUpdateView.as_view(), name='update'),
    path('', NutrientListView.as_view(),
             name='list'),
]
