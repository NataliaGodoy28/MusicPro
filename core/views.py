from django.shortcuts import render, redirect
from .models import *
from .forms import *
import MySQLdb

db = MySQLdb.connect(host='localhost', user='root', passwd='', db='musicpro')
boleta = 0

# Create your views here.


def index(request):
    datos = {
        'productos': Producto.objects.all()
    }
    return render(request, 'core/index.html', datos)


def bodeguero(request):
    return render(request, 'core/bodeguero.html')


def form_cliente(request):

    datos = {
        'form': ClienteForm()
    }

    if request.method == 'POST':
        formulario = ClienteForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            datos['mensaje'] = "Guardados correctamente"
    print(f"{Cliente.objects.all()}")
    return render(request, 'core/form_cliente.html', datos)


def contador(request):
    datos = {
        'registro': RegistroEntrega.objects.all(),
        'form': FRegistroEntrega()
    }
    if request.method == "POST":
        formu = FRegistroEntrega(request.POST)
        if formu.is_valid():
            formu.save()
            return redirect('contador')  # redireccionar a la misma vista
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
            usuario = Cliente.objects.filter(
                mailCliente__contains=login.cleaned_data["mailCliente"])
            contra = Cliente.objects.filter(
                claveCliente__contains=login.cleaned_data["claveCliente"])
            print(usuario)
            print(contra)
            return redirect(to='index')
    return render(request, 'core/login.html', datos)


def logout(request):
    return render(request, 'core/logout.html')


def boleta(request, id):
    global boleta
    boleta = Boleta.objects.all()
    detalleBoleta = DetalleBoleta.objects.filter(id_boleta=id)
    datos = {'detalle_boleta' : detalleBoleta, 'boleta': boleta}
    print("hola2")
    return render(request, 'core/bodeguero.html', datos)


def confirmarPedido(request):
    global boleta
    print("confirmar pedido")
    print("boleta :" +  str(boleta))
    cursor = db.cursor()
    bodeguero = "juanito"
    boleta = 0
    guia = 0
    estadopedido = "aceptado"

    # Crear la tupla con los valores a insertar
    purchases = (str(bodeguero), str(estadopedido), int(boleta),int(guia))

    # Ejecutar la consulta SQL y pasar la tupla de valores como parámetro
    cursor.execute('INSERT INTO core_estadopedido (id, fecha, bodeguero, estado, id_boleta_id, id_guia_id) VALUES (NULL, NULL, %s, %s, %s, %s)', (str(
        purchases[0]), str(purchases[1]), str(purchases[2]),str(purchases[3])))

    # Confirmar los cambios en la base de datos
    db.commit()

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    db.close()

    return render(request, 'core/bodeguero.html')


def cancelarPedido(request):
    print("cancelar pedido")
    
    cursor = db.cursor()
    bodeguero = "juanito"
    boleta = 9
    guia = 1
    estadopedido = "cancelado"

    # Crear la tupla con los valores a insertar
    purchases = (str(bodeguero), str(estadopedido), int(boleta),int(guia))

    # Ejecutar la consulta SQL y pasar la tupla de valores como parámetro
    cursor.execute('INSERT INTO core_estadopedido (id, fecha, bodeguero, estado, id_boleta_id, id_guia_id) VALUES (NULL, NULL, %s, %s, %s, %s)', (str(
        purchases[0]), str(purchases[1]), str(purchases[2]),str(purchases[3])))

    # Confirmar los cambios en la base de datos
    db.commit()

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    db.close()

    return render(request, 'core/bodeguero.html')
