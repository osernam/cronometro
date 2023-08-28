from django.urls import path
from .views import *

app_name = "cronometro"

urlpatterns = [
    path('index/', homeView, name='home'),
    path('login/', login, name = 'login'),
    path('logout/', logout, name = 'logout'),
    path('registro/', registro, name = 'registro'),
    path('save/', guardarUsuario, name = 'guardarUsuario'),
    
    path('cronometro/', cronometroView, name= 'cronometro'),
    path('selecOper/', selecOperario, name= 'selecOperario'),
    path('cronometro/cronometro/tiempo-parcial/', tiempo_parcial, name='tiempo-parcial'),
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
    
    
    path('cronometro/actualizar_datos/', actualizarDatos, name='actualizar_datos'),
    path('cronometro/informe_operario/<int:id>', generar_informe, name='generar_informe'),
]