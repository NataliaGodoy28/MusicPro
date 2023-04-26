from django.urls import path
from .views import *
#from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', index,name='index' ),
    #path('', plantillaGlobal, name="plantillaGlobal"),
    path('registroCliente', form_cliente, name="form_cliente"),
    path('contador', contador,name='contador'),
    path('bodeguero', bodeguero,name='bodeguero'),
    #path('login', LoginView.as_view(template_name="core/login.html")  ,  name='login' ),
    path('login', login, name='login'),
    path('logout', logout, name = 'logout')
]