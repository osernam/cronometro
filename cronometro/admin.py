from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Operario)
admin.site.register(Operacion)
admin.site.register(Maquina)
admin.site.register(OperacionOperario)