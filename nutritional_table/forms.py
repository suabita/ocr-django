from django.forms import ModelForm
from nutritional_table.models import NutritionalTable
from django import forms


class NutritionalTableForm(ModelForm):
    
    class Meta:
        model = NutritionalTable
        fields = ('file_table',)
        widgets = {
            'logo': forms.ClearableFileInput(attrs={
                'onchange': "readURL(this, '#id_table_img')",
                "accept": ".jpg, .png, .jpeg"
            })
        }
