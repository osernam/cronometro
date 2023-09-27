"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cronometro import views

urlpatterns = [
    path('', views.homeView, name='home'),  # Ruta raíz que llama a la función homeView
    path('admin/', admin.site.urls),
   # path('cronometro/', include('cronometro.urls')),
    
    
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    
    #recuperacion
    path('inicio_recuperar/', views.inicioRecuperacion, name = 'inicioRecuperacion'),
    path('correo/', views.correoRecuperacion, name = 'correoRecuperacion'),
    path('recuperar/', views.recuperar, name = 'recuperar'),
    path('restablecer_contrasena/<int:id>', views.formRestablecerContrasena, name = 'formRestablecerContrasena'),
    
    #Usuario
    path('registro/', views.registro, name = 'registro'),
    path('save/', views.guardarUsuario, name = 'guardarUsuario'),
    path('list_usuario/', views.listarUsuarios, name='listarUsuarios'),
    path('edit_usuario/<int:id>', views.actualizarUsuario, name='actualizarUsuario'),
    path('edicion_usuario/>', views.edicionUsuario, name='edicionUsuario'),
    path('estado_usuario/<int:id>', views.deshabilitarUsuario, name='deshabilitarUsuario'),
    
    #Cronometro
    path('cronometro/', views.cronometroView, name= 'cronometro'),
    path('selecOper/', views.selecOperario, name= 'selecOperario'),
    path('cronometro/cronometro/tiempo_parcial/', views.tiempo_parcial, name='tiempo-parcial'),
    path('cronometro/guardarTiempoEstandar/<int:id>',views.guardarTiempoEstandar , name= 'guardarTiempoEstandar'),
    path('cronometro/base/', views.base, name='base'),
    #operario
    path('operario/', views.crearOperario, name='crearOperario'),
    path('save_operario/', views.guardarOperario, name='guardarOperario'),
    path('mod_operario/', views.guardarTiempoParcial, name='guardarTiempoParcial'),
    path('list_operario/', views.listarOperarios, name='listarOperarios'),
    path('edit_operario/<int:id>', views.actualizarOperario, name='actualizarOperario'),
    path('edicion_operario/>', views.edicionOperario, name='edicionOperario'),
    path('estado_operario/<int:id>', views.deshabilitarOperario, name='deshabilitarOperario'),
    path('operario/historico/<int:id>', views.historial, name='historial'),
    path('operario/eliminar_historia/<int:id>', views.eliminarHistoria, name='eliminarHistoria'),
    
    #Maquina
    path('maquina/', views.crearMaquina, name='crearMaquina'),
    path('save_maquina/', views.guardarMaquina, name='guardarMaquina'),
    path('list_maquina/', views.listarMaquinas, name='listarMaquinas'),
    path('estado_maquina/<int:id>', views.deshabilitarMaquina, name='deshabilitarMaquina'),
    path('edit_maquina/<int:id>', views.actualizarMaquina, name='actualizarMaquina'),
    path('edicion_maquina/>', views.editarMaquina, name='editarMaquina'),
    
    #Operacion
    path('operacion/', views.crearOperacion, name='crearOperacion'),
    path('save_operacion/', views.guardarOperacion, name='guardarOperacion'),
    path('list_operacion/', views.listarOperaciones, name='listarOperaciones'),
    path('estado_operacion/<int:id>', views.deshabilitarOperacion, name='deshabilitarOperacion'),
    path('edit_operacion/<int:id>', views.actualizarOperacion, name='actualizarOperacion'),
    path('edicion_operacion/>', views.editarOperacion, name='editarOperacion'),
    
    
    #informe
    path('cronometro/generar_informe_operario/<int:id>', views.generarInforme, name='generarInforme'),
    path('buscar_operario/', views.buscarOperario, name='buscarOperario'),
]
