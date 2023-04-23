from django.urls import path
from .views import *

urlpatterns = [
    path('', index,name='index' ),
    path('', plantillaGlobal, name="plantillaGlobal"),
    path('registroCliente', form_cliente, name="form_cliente"),
    path('contador/', contador,name='contador')
]