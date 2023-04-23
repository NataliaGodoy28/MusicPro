from django.shortcuts import render
from .forms import ClienteForm
from .models import Cliente
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def plantillaGlobal(request):
    return render(request, 'core/plantillaGlobal.html')

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
            
