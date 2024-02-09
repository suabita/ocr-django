from django.forms import ModelForm
from nutrient.models import Nutrient


class NutrientForm(ModelForm):
    class Meta:
        model = Nutrient
        fields = ('name',)