from django.urls import path
from .views import index, plantillaGlobal, form_cliente

urlpatterns = [
    path('', index,name='index' ),
    path('', plantillaGlobal, name="plantillaGlobal"),
    path('registroCliente', form_cliente, name="form_cliente")
]