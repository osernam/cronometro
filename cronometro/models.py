from django.db import models
from datetime import date
from email.policy import default
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique = True)
    clave = models.CharField(max_length=254)
    roles_CHOISES = (('A', 'Administrador'), ('U', 'Usuario'))
    rol = models.CharField(max_length=20, choices=roles_CHOISES, default='U')
    fecha_nacimiento = models.DateField(default=date.today)
    estado = models.BooleanField(default=True)
    
     # Agregue related_name para resolver el conflicto
    groups = models.ManyToManyField(
        'auth.Group', related_name='usuario_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='usuario_set', blank=True
    )
    
    def __str__(self) -> str:
        return f"{self.nombre}"
    
class Operario(models.Model):
    nombre = models.CharField(max_length=50)
    entidad = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique = True)
    #tiemposMiliseg = models.BinaryField(blank=True, null=True)
    #tiemposNormales =models.BinaryField(blank=True, null=True) 
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    estado = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.nombre}"
    

class Maquina(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)    

class Operacion (models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    
class OperacionOperario(models.Model):
    idOperario = models.ForeignKey(Operario, on_delete=models.DO_NOTHING)
    idOperacion = models.ForeignKey(Operacion, on_delete=models.DO_NOTHING)
    idMaquinas = models.ForeignKey(Maquina, on_delete=models.DO_NOTHING)
    fechas = models.DateTimeField(auto_now_add=True, blank=True)
    tiempoEstandar = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    factorRitmo = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    uniHoras = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    escalaSuplementos = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return f"id: {self.id} - Fr {self.factorRitmo} - Es {self.escalaSuplementos}"
    
    