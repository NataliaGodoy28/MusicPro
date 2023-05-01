from django.db import models

# Create your models here.

#ModeloCliente

class Cliente(models.Model):
    idCliente = models.AutoField(primary_key=True, verbose_name="id de cliente")
    nombreCliente = models.CharField(max_length=50, verbose_name="nombre cliente")
    apellidoCliente = models.CharField(max_length=50, verbose_name="apellido cliente")
    mailCliente = models.CharField(max_length=60, verbose_name="email cliente")
    claveCliente=models.CharField(max_length=20, verbose_name="contraseña cliente")
    
    def __str__ (self):
        return self.mailCliente
    
class RegistroEntrega(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    identificador = models.CharField(max_length=255)
    contador = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    imagen = models.ImageField(upload_to='productos/')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre