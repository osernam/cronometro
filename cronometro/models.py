from django.db import models
from datetime import date
from email.policy import default

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique = True)
    clave = models.CharField(max_length=254)
    roles_CHOISES = (('A', 'Administrador'), ('U', 'Usuario'))
    rol = models.CharField(max_length=20, choices=roles_CHOISES, default='U')
    fecha_nacimiento = models.DateField(default=date.today)
    estado = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.nombre}"
    
class Operario(models.Model):
    nombre = models.CharField(max_length=50)
    entidad = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique = True)
    #tiemposMiliseg = models.BinaryField(blank=True, null=True)
    #tiemposNormales =models.BinaryField(blank=True, null=True) 
    tiempoEstandar = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    factorRitmo = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    escalaSuplementos = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    estado = models.BooleanField()
    
    def __str__(self) -> str:
        return f"{self.nombre}"