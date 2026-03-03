from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

INPUT_CLASS = 'border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:border-blue-500'
class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Correo electrónico", required=True,
        widget=forms.EmailInput(attrs={'class': INPUT_CLASS}))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 
                                                                                                INPUT_CLASS}))
    phone = forms.CharField(label='Teléfono', max_length=10, required=False, widget=forms.TextInput(attrs={
        'class': INPUT_CLASS,
        'type': 'tel',
        'pattern': '[0-9]{10}',
        'placeholder': '3001234567'
    }))


    address = forms.CharField(label='Dirección', max_length=200, required=False, widget=forms.TextInput(attrs=
                                                                                    {'class': INPUT_CLASS}))

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
    username = forms.CharField(label="Usuario", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))


class ProfileForm(forms.ModelForm):  #para editar los datos de mi perfil
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'image']
        labels = {
            'phone': 'Teléfono',
            'address': 'Dirección',
        }
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'border rounded-lg p-2 w-full text-sm text-gray-700',
                'accept': 'image/*',
        }),
}

