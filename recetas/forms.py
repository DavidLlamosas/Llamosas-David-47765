from django.forms import ModelForm
from .models import Publicaciones
from django import forms
from .models import Personas
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PublisForm(ModelForm):
    class Meta:
        model = Publicaciones
        fields = ['title', 'ingredientes', 'preparacion']
        exclude = ['fecha_actualizada']


class CalificacionForm(forms.Form):
    CALIFICACIONES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    calificacion = forms.ChoiceField(choices=CALIFICACIONES, widget=forms.RadioSelect, label='Calificación')

class UserEditForm(UserCreationForm):
    email = forms.EmailField(label="Ingrese su email:")
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir la contraseña', widget=forms.PasswordInput)
    last_name = forms.CharField()
    first_name = forms.CharField()
    
    class Meta:
            model = User
            fields = ['email', 'password1', 'password2',
            'last_name', 'first_name']

class AvatarForm(forms.Form):
    imagen = forms.ImageField(label="Imagen de Avatar")
    