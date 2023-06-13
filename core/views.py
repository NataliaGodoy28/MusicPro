from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponseRedirect

import requests
import uuid
boleta = 0
boletaGlobal = 0
boleta2 = 0

dolar = None


@csrf_exempt
def crearBoletacarro(request):

    
    if not request.session.get('usuario'):
        request.session['usuario'] = 'invitado'

    usuario = request.session['usuario']
    total_boleta = 0

    if request.method == 'POST':
        data = json.loads(request.body)
        cart_items = data.get("cartItems", [])
        pago = data.get("paymentMethod")
        productos = []

        for item in cart_items:
            productos.append({
                'codigo': item.get("code"),
                'nombre': item.get("title"),
                'cantidad': item.get("count"),
                'precio': item.get("price"),
                'imagen_url': item.get("img"),
            })

        if not productos:
            # Mostrar mensaje de error si el carrito está vacío
            messages.error(request, 'El carrito está vacío.', extra_tags='alert-danger')
            # Redireccionar al usuario a la página de vendedor
            return redirect('index')

        try:
            # Crear una nueva instancia de Boleta
            boleta = Boleta.objects.create(vendedor=usuario)

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
            boleta.tipo_pago = pago
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
                'precio_total_carrito': total_boleta,
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


def index(request):
    global dolar
    
    if dolar is None:
        valor_dolar()
   
    productos = Producto.objects.all()

    for producto in productos:
        precioD = float(producto.precio)
        producto.precio_dolar = round(precioD / float(dolar), 2)

    return render(request, 'core/index.html', {'productos': productos})


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



def valor_dolar():
    global dolar

    clave = "SmBc4syUBeoa"
    Usuario = "206039035"
    serie = "F073.TCO.PRE.Z.D"
    url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=206039035&pass=SmBc4syUBeoa&firstdate=2023-06-10&lastdate=2023-06-12&timeseries=F073.TCO.PRE.Z.D&function=GetSeries"

    response = requests.get(url)
    data = response.json()
    
    dolar = data.get("Series", {}).get("Obs", [])[0].get("value")


def prueba(request):
    global dolar
    
    if dolar is None:
        valor_dolar()

    precio = 5000
    total = round(precio / float(dolar), 2)
    data = {'api_data': total}

    return render(request, 'core/prueba.html', data)




# API WEBPAY PLUS
def get_ws(data, method, type, endpoint):
    if type == 'live':
        TbkApiKeyId = '597055555532'
        TbkApiKeySecret = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
        url = "https://webpay3g.transbank.cl" + endpoint  # Live
    else:
        TbkApiKeyId = '597055555532'
        TbkApiKeySecret = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
        url = "https://webpay3gint.transbank.cl" + endpoint  # Testing

    headers = {
        'Tbk-Api-Key-Id': TbkApiKeyId,
        'Tbk-Api-Key-Secret': TbkApiKeySecret,
        'Content-Type': 'application/json'
    }

    response = requests.request(method, url, headers=headers, data=data)
    return response.json()

def transbank(request):
    baseurl = request.build_absolute_uri('/')

    action = request.GET.get("action", "init")
    message = None

    # Generar el idSesion único
    id_sesion = str(uuid.uuid4())

    # Obtener el objeto Datos_compra correspondiente a la compra más reciente
    datos_compra = Boleta.objects.latest('id')
    total = datos_compra.total
    # Crear una instancia de la clase Carrito
    

    # Obtener el precio total del carrito
    
    if action == "init":
        message = 'init'
        amount = total
        return_url = baseurl + "?action=getResult"
        type = "sandbox"
        data = {
            "buy_order": datos_compra.id,
            "session_id": id_sesion,
            "amount": amount,
            "return_url": return_url
        }
        data = json.dumps(data)
        method = 'POST'
        endpoint = '/rswebpaytransaction/api/webpay/v1.2/transactions'

        response = get_ws(data, method, type, endpoint)
        token = response.get("token")
        url = response.get("url")
        redirect_url = f"{url}?token_ws={token}"
        return HttpResponseRedirect(redirect_url)

    elif action == "getResult":
        message = request.POST
        if 'token_ws' not in request.POST:
            return JsonResponse({'message': message})

        token = request.POST.get('token_ws')

        

        data = json.dumps({'token': token})
        method = 'PUT'
        type = 'sandbox'
        endpoint = f'/rswebpaytransaction/api/webpay/v1.2/transactions/{token}'

        response = get_ws(data, method, type, endpoint)
        return JsonResponse(response)

    elif action == "getStatus":
        message = request.POST
        if 'token_ws' not in request.POST:
            return JsonResponse({'message': message})

        token = request.POST.get('token_ws')
        data = json.dumps({'token': token})
        method = 'GET'
        type = 'sandbox'
        endpoint = f'/rswebpaytransaction/api/webpay/v1.2/transactions/{token}'
	
        response = get_ws(data, method, type, endpoint)
        return JsonResponse(response)

    elif action == "refund":
        message = request.POST
        if 'token_ws' not in request.POST:
            return JsonResponse({'message': message})

        token = request.POST.get('token_ws')
        amount = total

        data = json.dumps({'amount': amount})
        method = 'POST'
        type = 'sandbox'
        endpoint = f'/rswebpaytransaction/api/webpay/v1.2/transactions/{token}/refunds'

        response = get_ws(data, method, type, endpoint)
        return JsonResponse(response)

    return JsonResponse({'message': message})
