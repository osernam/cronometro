from django.urls import path
from .views import *

app_name = "cronometro"

urlpatterns = [
    path('index', homeView, name='home'),
    path('cronometro/', cronometroView, name= 'cronometro'),
    path('selecOper/', selecOperario, name= 'selecOperario'),
    path('cronometro/cronometro/tiempo-parcial/', tiempo_parcial, name='tiempo-parcial'),
    path('cronometro/guardarTiempoEstandar/<int:id>',guardarTiempoEstandar , name= 'guardarTiempoEstandar'),
    path('cronometro/base/', base, name='base'),
    path('operario/', crearOperario, name='crearOperario'),
    path('save_operario/', guardarOperario, name='guardarOperario'),
    path('mod_operario/', guardarTiempoParcial, name='guardarTiempoParcial'),
]