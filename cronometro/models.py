from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.IntegerField()
    estado=models.BooleanField()
    
class Operario(models.Model):
    nombre = models.CharField(max_length=50)
    entidad = models.CharField(max_length=50)
    tiempoEstandar = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateField()
    estado=models.BooleanField()