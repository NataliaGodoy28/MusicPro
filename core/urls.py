from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
#from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', index,name='index' ),
    #path('', plantillaGlobal, name="plantillaGlobal"),
    path('registroCliente', form_cliente, name="form_cliente"),
    path('contador', contador,name='contador'),
    path('bodeguero', bodeguero,name='bodeguero'),
    #path('login', LoginView.as_view(template_name="core/login.html")  ,  name='login' ),
    path('login', login, name='login'),
    path('logout', logout, name = 'logout'),
    path('confirmarPedido', confirmarPedido,name='confirmarPedido'),
    path('cancelarPedido', cancelarPedido,name='cancelarPedido'),
    path('boletas/<id>', boletas,name='boletas'),
    path('vendedor', vendedor ,name='vendedor'),
    path('añadirElemento', añadirElemento ,name='añadirElemento'),
    path('crearBoleta', crearBoleta ,name='crearBoleta'),
    path('generar_pago', generar_pago ,name='generar_pago'),
    path('verBoleta/<id>', verBoleta ,name='verBoleta'),
    path('detalle_boleta', detalle_boleta ,name='detalle_boleta'),
    path('productos', productos, name='productos'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('editar/<int:producto_id>/', editar_producto, name='editar_producto'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)