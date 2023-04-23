from .models import *
from django.forms import ModelForm
from .models import Cliente
from django import forms

class ClienteForm(ModelForm):
    
    class Meta:
        model = Cliente
        fields = ['nombreCliente','apellidoCliente','mailCliente','claveCliente']

class FRegistroEntrega(ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = RegistroEntrega
        fields = ['fecha','descripcion','cantidad','identificador','contador','cliente']
