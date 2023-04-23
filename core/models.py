from django.db import models

# Create your models here.

#ModeloCliente

class Cliente(models.Model):
    idCliente = models.IntegerField(primary_key=True, verbose_name="id de cliente")
    nombreCliente = models.CharField(max_length=50, verbose_name="nombre cliente")
    apellidoCliente = models.CharField(max_length=50, verbose_name="apellido cliente")
    mailCliente = models.CharField(max_length=60, verbose_name="email cliente")
    claveCliente=models.CharField(max_length=20, verbose_name="contraseña cliente")
    
    def __str__ (self):
        return self.mailCliente