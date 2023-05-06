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
    path('boleta/<id>', boleta,name='boleta'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)