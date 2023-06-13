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
    codigo = models.CharField(max_length=10, null=True,blank=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    detalle = models.TextField(default="detalle")
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    imagen = models.ImageField(upload_to='productos/')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre


class Boleta (models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField(null=True,blank=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    vendedor = models.CharField(max_length=40, null=True, blank=True)
    pago = models.IntegerField(null=True,blank=True)
    estado = models.BooleanField(default=False, null=True, blank=True)
    tipo_pago = models.CharField(max_length=40, null=True, blank=True)
    est_pago = models.CharField(max_length=40, null=True, blank=True)
    def __int__(self):
        return self.id


class DetalleBoleta(models.Model):

    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    producto =  models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=True, blank=True)
    precio_unitario = models.IntegerField()

    def __str__(self):
        return str(self.cantidad * self.precio_unitario)


class EstadoPedido (models.Model):
    id = models.AutoField(primary_key=True)
    id_boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    bodeguero = models.CharField(max_length=40, null=True, blank=True)
    vendedor = models.CharField(max_length=40, null=True, blank=True)
    estado = models.CharField(max_length=40, null=True, blank=True)
    estadoVendedor = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self)  :
        return self.estado
