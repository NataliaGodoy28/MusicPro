from decimal import Decimal
from django.shortcuts import render, redirect
import requests
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

boleta = 0
boletaGlobal = 0
boleta2 = 0

# Create your views here.
@csrf_exempt
def crearBoletacarro(request):
    if not request.session.get('usuario'):
        request.session['usuario'] = 'invitado'

    usuario = request.session['usuario']
    
    if request.method == 'POST':
        # Obtener el carrito
        carrito = request.session.get('carrito', {})
        productos = []

        # Calcular el total del carrito
        total_carrito = Decimal('0.00')

        for producto_carrito_id, cantidad in carrito.items():
            producto_id, session_key = producto_carrito_id.split('_')
            producto = get_object_or_404(Producto, id=producto_id)
            total_producto = cantidad * producto.precio

            productos.append({
                'id': producto_carrito_id,
                'codigo' : producto.codigo,
                'nombre': producto.nombre,
                'cantidad': cantidad,
                'precio': producto.precio,
                'imagen_url': producto.imagen.url,
                'precio_total_producto': total_producto,
            })

            total_carrito += total_producto

        if not productos:
            # Mostrar mensaje de error si el carrito está vacío
            messages.error(request, 'El carrito está vacío.', extra_tags='alert-danger')
            # Redireccionar al usuario a la página de vendedor
            return redirect('index')

        try:
            # Crear una nueva instancia de Boleta
            boleta = Boleta.objects.create(vendedor=usuario)

            # Insertar los productos del carrito en el detalle de la boleta
            total_boleta = Decimal('0.00')
            for producto_data in productos:
                codigo_producto = producto_data['codigo']
                cantidad = producto_data['cantidad']
                producto = get_object_or_404(Producto, codigo=codigo_producto)

                detalle_boleta = DetalleBoleta(
                    boleta=boleta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

                detalle_boleta.save()

                total_producto = producto.precio * cantidad
                total_boleta += total_producto

            # Guardar el total en la boleta

            boleta.total = total_boleta
            boleta.save()

            # Obtener todos los detalles de la boleta para mostrar en la vista
            detalles_boleta = DetalleBoleta.objects.filter(boleta=boleta)
            boletas = Boleta.objects.all().order_by('-id')

            datos = {
                'detalle': detalles_boleta,
                'boletas': boletas,
                'total_boleta': total_boleta,
                'productos': productos,
                'precio_total_carrito': total_carrito,
            }

            # Resto del código de la vista
            return render(request, 'core/index.html', datos)

        except Producto.DoesNotExist:
            # Mostrar mensaje de error personalizado
            messages.error(request, 'El producto no existe.', extra_tags='alert-danger')
            # Redireccionar al usuario a la página de vendedor
            return redirect('index')

    # Si el método HTTP no es POST, se muestra el formulario inicial o cualquier otra lógica que desees implementar
    return render(request, 'core/index.html')

def productos(request):
    datos = {
        'pformu': ProductoForms(),
        'productos': Producto.objects.all()
    }
    if request.method == "POST":
        pform = ProductoForms(request.POST, request.FILES)

        if pform.is_valid():
            # Guardar el formulario y obtener la instancia del modelo guardado
            instance = pform.save()
            print(f"Formulario guardado: {instance}")
            return redirect('productos')  # redireccionar a la misma vista
        else:
            print(pform.errors)  # Imprimir los errores del formulario
    return render(request, 'core/productos.html', datos)


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('productos')


def editar_producto(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        # Obtener los nuevos datos del producto del formulario
        nuevo_codigo = request.POST.get('nuevo_codigo')
        nuevo_nombre = request.POST.get('nuevo_nombre')
        nueva_descripcion = request.POST.get('nueva_descripcion')
        nuevo_stock = request.POST.get('nuevo_stock')
        nuevo_precio = request.POST.get('nuevo_precio')

        # Obtener la nueva imagen del formulario
        nueva_imagen = request.FILES.get('nueva_imagen')

        # Actualizar los campos del producto con los nuevos datos
        producto.codigo = nuevo_codigo
        producto.nombre = nuevo_nombre
        producto.descripcion = nueva_descripcion
        producto.stock = nuevo_stock
        producto.precio = nuevo_precio

        # Verificar si se proporcionó una nueva imagen
        if nueva_imagen:
            # Guardar la nueva imagen en el sistema de archivos
            filename = default_storage.save(nueva_imagen.name, nueva_imagen)
            producto.imagen = filename

        producto.save()

        # Redirigir a la vista deseada después de la edición
        return redirect('productos')

    return render(request, 'productos.html', {'producto': producto})


@csrf_exempt
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtener o crear el carrito de compras en la sesión
    carrito = request.session.get('carrito', {})

    # Verificar si el producto ya existe en el carrito
    producto_carrito_id = f"{producto_id}_{request.session.session_key}"
    carrito[producto_carrito_id] = carrito.get(producto_carrito_id, 0) + 1

    # Verificar si la cantidad es cero y eliminar el producto del carrito
    if carrito[producto_carrito_id] <= 0:
        del carrito[producto_carrito_id]

    # Actualizar el carrito en la sesión
    request.session['carrito'] = carrito

    # Calcular el precio total del carrito
    total_carrito = Decimal('0.00')
    for producto_carrito_id, cantidad in carrito.items():
        producto_id, session_key = producto_carrito_id.split('_')
        producto = get_object_or_404(Producto, id=producto_id)
        total_carrito += cantidad * producto.precio

    # Obtener el producto agregado al carrito
    producto_agregado = {
        'id': producto_carrito_id,
        'nombre': producto.nombre,
        'cantidad': carrito.get(producto_carrito_id, 0),
        'precio': producto.precio,
        'imagen_url': producto.imagen.url,
        'precio_total_carrito': total_carrito,
    }

    return JsonResponse(producto_agregado)


@csrf_exempt
def eliminar_del_carrito(request, producto_carrito_id):
    # Obtener o crear el carrito de compras en la sesión
    carrito = request.session.get('carrito', {})

    # Verificar si el producto existe en el carrito
    if producto_carrito_id in carrito:
        # Restar una unidad al producto del carrito
        carrito[producto_carrito_id] -= 1

        # Verificar si la cantidad es cero y eliminar el producto del carrito
        if carrito[producto_carrito_id] <= 0:
            del carrito[producto_carrito_id]

    # Actualizar el carrito en la sesión
    request.session['carrito'] = carrito

    # Calcular el precio total del carrito
    total_carrito = Decimal('0.00')
    for producto_carrito_id, cantidad in carrito.items():
        producto_id, session_key = producto_carrito_id.split('_')
        producto = get_object_or_404(Producto, id=producto_id)
        total_carrito += cantidad * producto.precio

    # Obtener el producto eliminado del carrito
    producto_eliminado = {
        'id': producto_carrito_id,
        'precio_total_carrito': total_carrito,
    }

    # Devolver una respuesta JSON con el producto eliminado y el precio total actualizado
    return JsonResponse(producto_eliminado)


@csrf_exempt
def obtener_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total_carrito = Decimal('0.00')

    for producto_carrito_id, cantidad in carrito.items():
        producto_id, session_key = producto_carrito_id.split('_')
        producto = get_object_or_404(Producto, id=producto_id)
        total_producto = cantidad * producto.precio

        productos.append({
            'id': producto_carrito_id,
            'nombre': producto.nombre,
            'cantidad': cantidad,
            'precio': producto.precio,
            'imagen_url': producto.imagen.url,
            'precio_total_producto': total_producto,
        })

        total_carrito += total_producto

    response_data = {
        'productos': productos,
        'precio_total_carrito': total_carrito,
    }

    return JsonResponse(response_data)


def index(request):
    productos = Producto.objects.all()
    carrito = request.session.get('carrito', {})
    productos_en_carrito = []

    total_carrito = Decimal('0.00')  # Inicializar el precio total del carrito

    for producto_carrito_id, cantidad in carrito.items():
        producto_id, carrito_id = producto_carrito_id.split(
            '_')  # Separar el producto_id y el carrito_id
        producto = get_object_or_404(Producto, id=producto_id)
        precio_producto = producto.precio * cantidad
        total_carrito += precio_producto

        productos_en_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'producto_carrito_id': producto_carrito_id,
            'precio_total': precio_producto  # Agregar el precio total al diccionario
        })

    datos = {
        'productos': productos,
        'productos_en_carrito': productos_en_carrito,
        'total_carrito': total_carrito  # Pasar el precio total del carrito a la plantilla
    }

    return render(request, 'core/index.html', datos)


@csrf_exempt
def reset_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
    return HttpResponse("El carrito se ha restablecido.")


def bodeguero(request):

    boletas_aceptadas = Boleta.objects.filter(estadopedido__estadoVendedor='Aceptado', estadopedido__estado__isnull=True).order_by('-id')


    # boletas_sin_aceptar = Boleta.objects.exclude(estadopedido__estado='Aceptado').order_by('-id')

    # boletas = Boleta.objects.all().order_by('-id')

    return render(request, 'core/bodeguero.html', {'boletas': boletas_aceptadas})


def detalle_boleta(request):
    boletas = Boleta.objects.all().order_by('-id')

    return render(request, 'core/detalle_boleta.html', {'boletas': boletas})


def detalle_boleta_vendedor(request):
    boletas = Boleta.objects.all().order_by('-id')

    return render(request, 'core/detalleBoletaVendedor.html', {'boletas': boletas})


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
            if usuario.exists() and contra.exists():
                # Almacena el ID del usuario en la sesión
                request.session['usuario'] = usuario.first().idCliente
                return redirect(to='index')

    return render(request, 'core/login.html', datos)


def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    return render(request, 'core/logout.html')


def boletas(request, id):
    global boleta2
    global boleta
    boletas_aceptadas = Boleta.objects.filter(estadopedido__estadoVendedor='Aceptado', estadopedido__estado__isnull=True).order_by('-id')

    # boletas_sin_aceptar = Boleta.objects.filter(estadopedido__estadoVendedor='Aceptado').order_by('-id')
    boletas = Boleta.objects.all().order_by('-id')
    print("boletas")
    boleta2 = id
    print(boleta2 + "boleta2")
    detalleBoleta = DetalleBoleta.objects.filter(boleta=id)
    # datos = {'detalle_boleta': detalleBoleta, 'boletas': boletas}
    datos = {'detalle_boleta': detalleBoleta, 'boletas': boletas_aceptadas}

    print("hola2")
    return render(request, 'core/bodeguero.html', datos)


def confirmarPedido(request):
    global boleta2
    print("confirmar pedido")
    print(boleta2)

    estado_pedido = get_object_or_404(EstadoPedido, id_boleta=boleta2)
    # bol = get_object_or_404(Boleta, id=boleta2)
    # print(bol)
    # print("boleta")
    # Establecer los valores de los campos
    # estado_pedido.id_boleta = bol
    # guia = GuiaBodeguero.objects.get(id_boleta_id=bol)

    # estado_pedido.fecha = tu_fecha
    estado_pedido.bodeguero = "Bodeguero 1"
    estado_pedido.estado = "Aceptado"

    # Guardar el objeto en la base de datos
    estado_pedido.save()

    return redirect('bodeguero')


def confirmarPedidoVendedor(request):
    global boleta2
    print(boleta2)
    print("confirmar pedido")
    print(boleta2)

    estado_pedido = EstadoPedido()
    bol = get_object_or_404(Boleta, id=boleta2)
    print(bol)
    print("boleta")
    # Establecer los valores de los campos
    estado_pedido.id_boleta = bol
    # guia = GuiaBodeguero.objects.get(id_boleta_id=bol)

    # estado_pedido.fecha = tu_fecha
    estado_pedido.vendedor = "vendedor 1"
    estado_pedido.estadoVendedor = "Aceptado"

    # Guardar el objeto en la base de datos
    estado_pedido.save()

    return redirect('vendedorProducto')


def cancelarPedido(request):
    global boleta2
    print("cancelar pedido")
    print(boleta2)

    estado_pedido = get_object_or_404(EstadoPedido, id_boleta=boleta2)
    # bol = get_object_or_404(Boleta, id=boleta2)
    # print(bol)
    # print("boleta")
    # Establecer los valores de los campos
    # estado_pedido.id_boleta = bol
    # guia = GuiaBodeguero.objects.get(id_boleta_id=bol)

    # estado_pedido.fecha = tu_fecha
    estado_pedido.bodeguero = "Bodeguero 1"
    estado_pedido.estado = "Cancelado"

    # Guardar el objeto en la base de datos
    estado_pedido.save()

    return redirect('bodeguero')


def cancelarPedidoVendedor(request):
    global boleta2
    print("cancelar pedido")
    print(boleta2)

    estado_pedido = EstadoPedido()
    bol = get_object_or_404(Boleta, id=boleta2)
    print(bol)
    print("boleta")
    # Establecer los valores de los campos
    estado_pedido.id_boleta = bol
    # guia = GuiaBodeguero.objects.get(id_boleta_id=bol)

    # estado_pedido.fecha = tu_fecha
    estado_pedido.vendedor = "vendedor 1"
    estado_pedido.estadoVendedor = "Cancelado"

    # Guardar el objeto en la base de datos
    estado_pedido.save()

    return redirect('vendedorProducto')


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


def verBoleta(request, id):

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

def boletaAceptada(request, id):

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

    return render(request, 'core/boletaAceptada.html', datos)


def verBoletaVendedor(request, id):

    print(id)
    global boletaGlobal
    # Obtener la boleta correspondiente
    boletas = Boleta.objects.filter(id=id)
    detalle = DetalleBoleta.objects.filter(boleta=id)
    print(boletas)
    global boleta2
    boleta2 = id

    datos = {
        'detalle': detalle,
        'boletas': boletas,
        'abrir_modal': True  # Agrega este valor al contexto

    }

    return render(request, 'core/detalleBoletaVendedor.html', datos)


def vendedorProducto(request):
    productos = Producto.objects.all()

    boletas_aceptadas = Boleta.objects.filter(estadopedido__estadoVendedor='Aceptado', estadopedido__estado='Aceptado').order_by('-id')


    boletas = Boleta.objects.filter(estadopedido__estadoVendedor__isnull=True)
    # boletas = Boleta.objects.all()
    datos = {
        'productos': productos,
        'boletas': boletas,
        'boletasAceptadas':boletas_aceptadas}

    return render(request, 'core/vendedorProducto.html', datos)


def prueba(request):
    response = requests.get('https://cmvapp.cl/listarDelegado.php')
    data = response.json()
    data = {'api_data': data} 

    return render(request, 'core/prueba.html', data)