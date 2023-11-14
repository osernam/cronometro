from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Usuario, Empresa
#Libreria para encripación
from passlib.context import CryptContext
# Round: Iteraciones para reducir la posibilidad de cracking.
contexto = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=333
)


@receiver(post_migrate)
def crear_usuario_por_defecto(sender, **kwargs):
    if Usuario.objects.count() == 0:
        # La tabla de empresas está vacía, crea una empresa por defecto
        empresaAdm =Empresa(
                nombre= "CronometroADM",
                nit= 0000000000,
                estado=True
        )
        empresaAdm.save()
        
        # La tabla de usuarios está vacía, crea un usuario por defecto
        correo= "adm95193241@gmail.com"
        administrador =Usuario(
                email= correo,
                nombre= "admincronte",
                apellido= " adm",
                clave = contexto.hash("o36MB07VHV") ,
                password= contexto.hash("o36MB07VHV"),
                username= correo,
                rol= "A",
                estado=True,
                idEmpresa= Empresa.objects.get(id = 1),
                
            )
        administrador.save()
        