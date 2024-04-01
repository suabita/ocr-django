from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm
from authentication.user.models import User
from authentication.user.models import PhysiologicalChoices, GenderChoices
from django import forms


class SignUpForm(ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'required': True,
            'placeholder': _('Password'),
            'class': 'form-control'
        }),
        strip=False,
    )

    password2 = forms.CharField(
        label=_('Password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'required': True,
            'placeholder': _('Password confirmation'),
            'class': 'form-control'
        }),
    )

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean_first_name(self):
        print(self.cleaned_data['first_name'].capitalize())
        return self.cleaned_data['first_name'].capitalize()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()
    
    def clean(self):
        cleaned_data = super().clean()
        print("clean", cleaned_data)

        if cleaned_data.get('password1', True) != cleaned_data.get('password2', False):
            self.add_error('password1', _("The two password fields didn't match."))

    def save(self, commit=True):
        user = super().save(commit=False)  # No guardar en la base de datos todavía
        print("entro save")
        username = user.email.split('@')[0]

        if not User.objects.filter(username=username).exists():
            user.username = username
        else:
            user.username = user.email

        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()  # Guardar en la base de datos solo si se especifica commit=True

        return user

    
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "weight", 
                  "height", "sex", "age", "physiological_state", "physical_activity")
        widgets = {
            'email': forms.EmailInput(attrs={
                'autofocus': True,
                'required': True,
                'placeholder': _('email'),
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('first name'),
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('last name'),
                'class': 'form-control'
            }),
            'weight': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('weight'),
                'class': 'form-control'
            }),
            'height': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('height'),
                'class': 'form-control'
            }),
            'age': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('age'),
                'class': 'form-control'
            }),
            'physiological_state': forms.Select(attrs={
                'readonly': 'readonly',
                'class': 'form-control'
            }),
            'sex': forms.Select(attrs={
                'readonly': 'readonly',
                'class': 'form-control'
            }),
            
        }

class ProfileForm(ModelForm):
    #sex = forms.ChoiceField(label=_("gender"), choices=GenderChoices)
    #physiological_state = forms.ChoiceField(label=_("physiological state"), choices=PhysiologicalChoices)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "weight", 
                  "height", "sex", "age", "physiological_state", "physical_activity")
        widgets = {
            'username': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control'
                }),
            'first_name': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('first name'),
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('last name'),
                'class': 'form-control'
            }),
            'weight': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('weight'),
                'class': 'form-control'
            }),
            'height': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('height'),
                'class': 'form-control'
            }),
            'age': forms.TextInput(attrs={
                'required': True,
                'placeholder': _('age'),
                'class': 'form-control'
            }),
            'physiological_state': forms.Select(attrs={
                'readonly': 'readonly',
                'class': 'form-control'
            }),
            'physcal_activity': forms.Select(attrs={
                'readonly': 'readonly',
                'class': 'form-control'
            }),
            'sex': forms.Select(attrs={
                'readonly': 'readonly',
                'class': 'form-control'
            }),
            
        }