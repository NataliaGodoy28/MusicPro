from django.shortcuts import render, redirect
from .models import *
from .forms import *
import MySQLdb
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


db = MySQLdb.connect(host='localhost', user='root', passwd='', db='musicpro')
boleta = 0
boletaGlobal = 0

# Create your views here.


def index(request):
    datos = {
        'productos': Producto.objects.all()
    }
    return render(request, 'core/index.html', datos)


def bodeguero(request):
    boletas = Boleta.objects.all().order_by('-id')

    return render(request, 'core/bodeguero.html', {'boletas': boletas})

def detalle_boleta(request):
    boletas = Boleta.objects.all().order_by('-id')

    return render(request, 'core/detalle_boleta.html', {'boletas': boletas})
 
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
        'confirmar': EstadoPedido.objects.filter(estado='Pendiente'),
        'registro': RegistroEntrega.objects.all(),
        'form': FRegistroEntrega()
    }
    if request.method == "POST":
        formu = FRegistroEntrega(request.POST)
        if formu.is_valid():
            formu.save()
            return redirect('contador')  # redireccionar a la misma vista
    return render(request, 'core/contador.html', datos)


def actualizar_estado_pedido(request, pedido_id, nuevo_estado):
    # Obtener el pedido que se desea actualizar
    pedido = EstadoPedido.objects.filter(id=pedido_id).first()

    # Verificar si el pedido existe
    if not pedido:
        # Manejar la situación donde el pedido no existe
        return redirect('pagina_de_error')

    # Actualizar el estado del pedido
    pedido.estado = nuevo_estado

    # Guardar los cambios en la base de datos
    pedido.save()

    # Redireccionar a la página correspondiente
    return redirect('contador')


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


def boletas(request, id):
    global boleta
    boletas = Boleta.objects.all().order_by('-id')
    print("boletas")
    detalleBoleta = DetalleBoleta.objects.filter(boleta=id)
    datos = {'detalle_boleta': detalleBoleta, 'boletas': boletas}
    print("hola2")
    return render(request, 'core/bodeguero.html', datos)


def confirmarPedido(request):
    global boleta
    print("confirmar pedido")
    print("boleta :" + str(boleta))
    cursor = db.cursor()
    bodeguero = "juanito"
    boleta = 0
    guia = 0
    estadopedido = "aceptado"

    # Crear la tupla con los valores a insertar
    purchases = (str(bodeguero), str(estadopedido), int(boleta), int(guia))

    # Ejecutar la consulta SQL y pasar la tupla de valores como parámetro
    cursor.execute('INSERT INTO core_estadopedido (id, fecha, bodeguero, estado, id_boleta_id, id_guia_id) VALUES (NULL, NULL, %s, %s, %s, %s)', (str(
        purchases[0]), str(purchases[1]), str(purchases[2]), str(purchases[3])))

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
    purchases = (str(bodeguero), str(estadopedido), int(boleta), int(guia))

    # Ejecutar la consulta SQL y pasar la tupla de valores como parámetro
    cursor.execute('INSERT INTO core_estadopedido (id, fecha, bodeguero, estado, id_boleta_id, id_guia_id) VALUES (NULL, NULL, %s, %s, %s, %s)', (str(
        purchases[0]), str(purchases[1]), str(purchases[2]), str(purchases[3])))

    # Confirmar los cambios en la base de datos
    db.commit()

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    db.close()

    return render(request, 'core/bodeguero.html')


def vendedor(request):

    boletas = Boleta.objects.all().order_by('-id')

    return render(request, 'core/vendedor.html', {'boletas': boletas})


@login_required
def crearBoleta(request):

    usuario = request.user
    # Crear una nueva instancia de Boleta
    # boletas = Boleta.objects.all()
    boletas = Boleta.objects.all().order_by('-id')
    bol = Boleta.objects.create(vendedor=usuario)
    global boletaGlobal
    boletaGlobal = bol.id
    # Resto del código de la vista
    print(boletaGlobal)
    # Por ejemplo, redireccionar al usuario a la página de detalle de la nueva boleta
    # return redirect('añadirElemento')
    return render(request, 'core/vendedor.html', {'boletas': boletas})


def añadirElemento(request):
    global boletaGlobal

    usuario = request.user

    if request.method == 'POST':
        # Obtener el código del producto ingresado por el usuario
        codigo_producto = request.POST.get('codigo_producto')
        unidad = request.POST.get('unidad')

        if not codigo_producto or not unidad:
            # Mostrar mensaje de error si los campos están vacíos
            messages.error(
                request, 'Los campos no pueden estar vacíos.', extra_tags='alert-danger')

            # Redireccionar al usuario a la página de vendedor
            return redirect('vendedor')

        try:
            # Buscar el producto en la base de datos
            producto = Producto.objects.get(codigo=codigo_producto)

            # Obtener la boleta actual o redirigir al usuario a la página de creación de una nueva boleta
            try:
                boleta = Boleta.objects.get(id=boletaGlobal, vendedor=usuario)
            except Boleta.DoesNotExist:
                messages.warning(
                    request, 'Debes generar una boleta', extra_tags='alert-danger')
                return redirect('vendedor')

            # Crear una nueva instancia de DetalleBoleta vinculada a la boleta y al producto
            detalle_boleta = DetalleBoleta(
                boleta=boleta, producto=producto, cantidad=unidad, precio_unitario=producto.precio)
            detalle_boleta.save()

            # Recalcular el total de la boleta
            detalles = DetalleBoleta.objects.filter(boleta=boleta)
            total_boleta = sum(detalle.producto.precio *
                               detalle.cantidad for detalle in detalles)
            boleta.total = total_boleta
            boleta.save()

            # Obtener todos los detalles de la boleta para mostrar en la vista
            detalles_boleta = DetalleBoleta.objects.filter(boleta=boleta)
            boletas = Boleta.objects.all().order_by('-id')

            datos = {
                'detalle': detalles_boleta,
                'boletas': boletas,
                'total_boleta': total_boleta
            }

            # Resto del código de la vista
            return render(request, 'core/vendedor.html', datos)

        except Producto.DoesNotExist:
            # Mostrar mensaje de error personalizado
            messages.error(request, 'El producto no existe.',
                           extra_tags='alert-danger')

            # Redireccionar al usuario a la página de vendedor
            return redirect('vendedor')

    # Si el método HTTP no es POST, se muestra el formulario inicial o cualquier otra lógica que desees implementar
    return render(request, 'core/vendedor.html')


def generar_pago(request):

    global boletaGlobal

    # Obtener la boleta correspondiente
    boletas = Boleta.objects.get(id=boletaGlobal)
    print(boletas)

    # Actualizar el estado de la boleta a True
    boletas.estado = True
    boletas.save()

    return redirect('vendedor')


def verBoleta(request,id):

    print(id)
    global boletaGlobal

    # Obtener la boleta correspondiente
    boletas = Boleta.objects.filter(id=id)
    detalle = DetalleBoleta.objects.filter(boleta=id)
    print(boletas)

    datos = {
        'detalle': detalle,
        'boletas': boletas,
        'abrir_modal': True  # Agrega este valor al contexto

    }

    return render(request, 'core/detalle_boleta.html', datos)
