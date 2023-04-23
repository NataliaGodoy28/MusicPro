from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def contador(request):
    registro = RegistroEntrega.objects.all()
    datos = {
        'registro' : registro
    }
    return render(request, 'core/contador.html', datos)
