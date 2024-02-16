from django.forms import ModelForm
from nutritional_table.models import NutritionalTable
from django import forms
from django.utils.translation import gettext_lazy as _



class NutritionalTableForm(ModelForm):
    
    class Meta:
        model = NutritionalTable
        fields = ('name', 'file_table',)
        widgets = {
            'file_table': forms.ClearableFileInput(attrs={
                'onchange': "readURL(this, '#id_table_img')",
                "accept": ".jpg, .png, .jpeg"
            }),
            'name': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('name'),
                'class': 'form-control'
            }),
        }
        