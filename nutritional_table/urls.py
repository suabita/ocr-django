from django.urls import path
from nutritional_table.views import NutritionalTableCreateView
from django.views.generic import TemplateView


app_name = 'nutrient'

urlpatterns = [
    path('create/', NutritionalTableCreateView.as_view(),
             name='create'),
    #path('update/<slug>/', NutrientUpdateView.as_view(), name='update'),
    #path('', NutrientListView.as_view(),
    #         name='list'),
]
