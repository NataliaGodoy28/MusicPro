from .models import *
from django.forms import ModelForm
from .models import Cliente
from django import forms

class ClienteForm(ModelForm):
    
    class Meta:
        model = Cliente
        fields = ['nombreCliente','apellidoCliente','mailCliente','claveCliente','direccion']

class FRegistroEntrega(ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = RegistroEntrega
        fields = ['fecha','descripcion','cantidad','identificador','contador','cliente']

class Login(ModelForm):
    claveCliente = forms.CharField(widget=forms.PasswordInput());
    class Meta:
        model = Cliente
        fields = ['mailCliente', 'claveCliente']

class ProductoForms(ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo','nombre','descripcion','stock','imagen','precio','categoria']

class InvitadoForms(ModelForm):
    class Meta:
        model = Invitado
        fields = ['correo','direccion']

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']