from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    phone = forms.CharField(label='Teléfono', max_length=10, required=False)
    address = forms.CharField(label='Dirección', max_length=200, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2
    
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):  #para editar los datos de mi perfil
    class Meta:
        model = Profile
        fields = ['phone', 'address']
        labels = {
            'phone': 'Teléfono',
            'address': 'Dirección',
        }
