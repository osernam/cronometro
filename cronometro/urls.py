from django.urls import path
from .views import *

app_name = "cronometro"

urlpatterns = [
    path('index/', homeView, name='home'),
    path('login/', login, name = 'login'),
    path('logout/', logout, name = 'logout'),
    #Usuario
    path('registro/', registro, name = 'registro'),
    path('save/', guardarUsuario, name = 'guardarUsuario'),
    
    path('list_usuario/', listarUsuarios, name='listarUsuarios'),
    path('edit_usuario/<int:id>', actualizarUsuario, name='actualizarUsuario'),
    path('edicion_usuario/>', edicionUsuario, name='edicionUsuario'),
    path('estado_usuario/<int:id>', deshabilitarUsuario, name='deshabilitarUsuario'),
    
    #Cronometro
    path('cronometro/', cronometroView, name= 'cronometro'),
    path('selecOper/', selecOperario, name= 'selecOperario'),
    path('cronometro/cronometro/tiempo_parcial/', tiempo_parcial, name='tiempo-parcial'),
    path('cronometro/guardarTiempoEstandar/<int:id>',guardarTiempoEstandar , name= 'guardarTiempoEstandar'),
    path('cronometro/base/', base, name='base'),
    #operario
    path('operario/', crearOperario, name='crearOperario'),
    path('save_operario/', guardarOperario, name='guardarOperario'),
    path('mod_operario/', guardarTiempoParcial, name='guardarTiempoParcial'),
    path('list_operario/', listarOperarios, name='listarOperarios'),
    path('edit_operario/<int:id>', actualizarOperario, name='actualizarOperario'),
    path('edicion_operario/>', edicionOperario, name='edicionOperario'),
    path('estado_operario/<int:id>', deshabilitarOperario, name='deshabilitarOperario'),
    
    
    #informe
    path('cronometro/generar_informe_operario/<int:id>', generarInforme, name='generarInforme'),
]