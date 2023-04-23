from django import forms
from django.forms import ModelForm
from .models import *

class FRegistroEntrega(ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = RegistroEntrega
        fields = ['fecha','descripcion','cantidad','identificador','contador','cliente']