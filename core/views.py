from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.

def index(request):
    datos = {
        'productos' : Producto.objects.all()
    }
    return render(request, 'core/index.html', datos)

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
            return redirect('contador') # redireccionar a la misma vista
    return render(request, 'core/contador.html', datos)


def login(request):
    print(f"{request.POST.getlist('tags')}")
    datos = {
        'form': Login()
    }
    
    if request.method == "POST":
        login = Login(request.POST)
        if login.is_valid():
            print("sdxdssxaxadadxad")
            usuario = Cliente.objects.filter(mailCliente__contains=login.cleaned_data["mailCliente"])
            contra =  Cliente.objects.filter(claveCliente__contains=login.cleaned_data["claveCliente"])
            print(usuario)
            print(contra)
            return redirect(to='index')
    return render(request, 'core/login.html', datos)

def logout(request):
    return render(request, 'core/logout.html')