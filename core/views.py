from django.shortcuts import render
from .models import *
from .forms import *
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def bodeguero(request):
    return render(request, 'core/bodeguero.html')

def form_cliente(request):
    
    datos = {
        'form': ClienteForm()
    }
    
    if request.method== 'POST':
        formulario = ClienteForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            datos['mensaje'] = "Guardados correctamente"
    print(f"{Cliente.objects.all()}")
    return render(request, 'core/form_cliente.html', datos)
            
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
