from django.shortcuts import render
from .models import *
from .forms import *
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def contador(request):
    datos = {
        'registro' : RegistroEntrega.objects.all(),
        'form' : FRegistroEntrega()
    }
    if request.method == "POST":
        formu = FRegistroEntrega(request.POST)
        if formu.is_valid():
            formu.save()
            datos['mensaje'] = "Entrega Registrada Correctamente"
    return render(request, 'core/contador.html', datos)
