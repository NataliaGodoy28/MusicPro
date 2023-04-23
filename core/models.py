from django.db import models

# Create your models here.
class RegistroEntrega(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    identificador = models.CharField(max_length=255)
    contador = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)