from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.db.models import Q
# Mensajes tipo cookies temporales
from django.contrib import messages
from django import forms
# Gestión de errores de base de datos
from django.db import IntegrityError  
# Paginador
from django.core.paginator import Paginator 
import json 
from django.core.serializers.json import DjangoJSONEncoder
#informe operario excel

from openpyxl import Workbook
import pytz
from django.utils import timezone

#Libreria para encripación
from passlib.context import CryptContext
# Round: Iteraciones para reducir la posibilidad de cracking.
contexto = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=333
)


# Create your views here.



def homeView(request):
    """
    Renderiza la vista de inicio.

    Argumentos:
        solicitud (HttpRequest): el objeto de solicitud HTTP.
    
    Devoluciones:
        HttpResponse: la respuesta HTML representada.
    """
    return render(request,'cronometro\index.html')

def selecOperario (request):
    """
    Representa la plantilla 'selec_operario.html' con la solicitud dada.

    Parámetros:
        solicitud (HttpRequest): el objeto de solicitud HTTP.
    
    Devoluciones:
        HttpResponse: el objeto de respuesta HTTP.
    """
    operarios = Operario.objects.all()
    maquinas = Maquina.objects.all()
      
    #datos_json = json.dumps(list(datos), cls=DjangoJSONEncoder)
    #return render(request, 'cronometro\operario\selec_operario.html', {
     #   'datos_json': datos_json,
      #  'operarios' : operarios
    #})
        
    return render(request,'cronometro\operario\selec_operario.html', {'operarios' : operarios , 'maquinas' : maquinas})


def login (request):
    """
    Esta función es responsable de manejar la solicitud de inicio de sesión.

    Argumentos:
        solicitud (HttpRequest): el objeto de solicitud HTTP.

    Devoluciones:
        HttpResponseRedirect: una respuesta de redireccionamiento a la página de inicio.

    Sube:
        Usuario.DoesNotExist: Si el usuario no existe.
    """
    if request.method == "POST":
        try:
            
            email = request.POST['email']
            clavePost = request.POST['clave']
            clave= contexto.hash(clavePost)       
            usuario = Usuario.objects.get(email = email)
            
            if contexto.verify(clavePost, usuario.clave):
                request.session["logueoUsuario"] = [usuario.id, usuario.nombre, usuario.apellido, usuario.email, usuario.get_rol_display()]       
                # -------------
                messages.success(request, "Bienvenido")
            else:
                messages.warning(request, "Contraseña incorrecta")
                
            return redirect('cronometro:home')
        except Usuario.DoesNotExist:
            messages.warning(request, "El usuario no existe")
            return redirect('cronometro:home')
        except Exception as e:
            messages.warning(request, e)
            return redirect('cronometro:home')
    else:
        messages.warning(request, "Usted no ha enviado datos")
        return redirect('cronometro:home')
    
def registro(request):
    
    """
    sigup
    renderiza el template  para registrar usuario

    Args:
        request (_type_): _description_

    Returns:
        _type_:  rendeiza la pagina sig-up.html
    """
    return render(request, 'cronometro/usuario/registro_usuario.html')
    

def guardarUsuario(request):
    """
    Guarda un usuario en la base de datos.
    Parameters:
    request (HttpRequest): La solicitud HTTP recibida.
    Returns:
    HttpResponseRedirect: Redirige al usuario hacia la página home si el usuario se guarda correctamente.
    """
    
    try: 
        if request.method == "POST":
            usuario = Usuario(
                email= request.POST['email'],
                nombre= request.POST['nombre'],
                apellido= request.POST['apellido'],
                fecha_nacimiento=request.POST['fecha_nacimiento'],
                clave = contexto.hash(request.POST['clave']) ,
                
            )
            usuario.full_clean()
            usuario.save()
            messages.success(request, f"Operari@ ha sido creado con éxito")
        
        else:
            messages.warning(request, "Usted no ha enviado datos")
    
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect('cronometro:registro')
        
    return redirect('cronometro:home')  

def listarUsuarios(request):
    """
    La función ListarUsuarios se encarga de recuperar y paginar una lista de usuarios de la base de datos.

    Parámetros:
        - solicitud: el objeto de solicitud que contiene información sobre la solicitud HTTP actual.
    
    Devoluciones:
        - Si el usuario ha iniciado sesión, devuelve la lista renderizada de usuarios usando la plantilla 'cronometro/usuario/listado_usuarios.html'.
        - Si el usuario no ha iniciado sesión, redirige a la URL 'cronometro:home' después de mostrar un mensaje de advertencia.
    """
    login = request.session.get('logueoUsuario', False)
    if login:
        usuarios = Usuario.objects.order_by('-estado')
        paginator = Paginator(usuarios, 10)
        page_number = request.GET.get('page')
        usuarios = paginator.get_page(page_number)
        return render(request, 'cronometro/usuario/listado_usuarios.html', {'usuarios' : usuarios})
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('cronometro:home')

def actualizarUsuario(request, id):
    """
    Actualiza un usuario en la base de datos con el ID proporcionado.

    Argumentos:
        solicitud (HttpRequest): el objeto de solicitud HTTP.
        id (int): El ID del usuario que se va a actualizar.
    
    Devoluciones:
        HttpResponse: la página HTML representada para editar el usuario si el usuario ha iniciado sesión y tiene permiso.
        De lo contrario, redirige a la página de lista de usuarios con un mensaje de advertencia.
    """
    login = request.session.get('logueoUsuario', False)
    if login:
        if login:
            usuario = Usuario.objects.get(id = id)
            return render(request, 'cronometro/usuario/edicion_usuario.html', {'usuario': usuario})
        else:
            messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('cronometro:listarUsuarios')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('cronometro:home')

def edicionUsuario(request):
    """
    Edite un usuario en el sistema según la solicitud proporcionada.

    Argumentos:
        solicitud (HttpRequest): el objeto de solicitud que contiene los datos del usuario.

    Devoluciones:
        HttpResponse: una respuesta de redireccionamiento a la página de lista de usuarios.
    """
    try:
        login = request.session.get('logueoUsuario', False)
        if login:
            if login:
                if request.method == "POST":
                    usuario = Usuario.objects.get(id = request.POST['id'])
                    
                    usuario.nombre = request.POST['nombre']
                    usuario.apellido = request.POST['apellido']
                    #usuario.rol = request.POST['rol']
                    usuario.estado = request.POST['estado']
                    
                    usuario.save()
                    messages.success(request, f"usuario ({usuario.nombre})  editado exitosamente")
                else:
                    messages.warning(request, "Usted no ha enviado datos")
            else:
                messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
                return redirect('cronometro:listarUsuarios')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarUsuarios')



def deshabilitarUsuario(request, id):
    """
    Deshabilita a un usuario según su ID.

    Argumentos:
        solicitud: el objeto de solicitud HTTP.
        id: El ID del usuario que se va a deshabilitar.

    Devoluciones:
        HttpResponseRedirect: Redirección a la vista 'listarUsuarios'.

    Sube:
        Excepción: Si hay un error durante el proceso.
    """
    try:
        login = request.session.get('logueoUsuario', False)
        if login:
            usuario = Usuario.objects.get(id = id)
            if usuario.estado == True:
                usuario.estado = False
            else:
                usuario.estado = True
            
            usuario.save()
            messages.success(request, f"Proveedor ({usuario.nombre}) modificado exitosamente")
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarUsuarios')



def logout(request):
    """
    Elimina la clave 'logueoUsuario' del diccionario de sesión y redirige
    al usuario a la URL 'cronometro:home'.

    Parámetros:
        solicitud (HttpRequest): el objeto de solicitud HTTP.

    Devoluciones:
        HttpResponseRedirect: una respuesta de redireccionamiento a la URL 'cronometro:home'.
    """
    del request.session['logueoUsuario']
    return redirect('cronometro:home')
    
def cronometroView(request):
    """
    Representa la plantilla 'cronometro.html' con una lista de todos los objetos 'Operario' 'maquina' y 'operacion'.

    parámetro: 
        el objeto de solicitud HTTP.
    return: 
        La plantilla HTML renderizada.
    """
    operarios = Operario.objects.all()
    maquina = Maquina.objects.all()
    operacion = Operacion.objects.all()
    return render(request,'cronometro\cronometro.html', {'operarios' : operarios , 'maquina' : maquina, 'operacion' : operacion})

def tiempo_parcial(request):
    """
    Esta función maneja la solicitud 'tiempo_parcial'.

    Argumentos:
        solicitud (HttpRequest): el objeto de solicitud HTTP.

    Devoluciones:
        JsonResponse: La respuesta JSON con el estado de la solicitud.
    """
    if request.method == "POST":
        tiempoParcial = request.POST.get('tiempoParcial')
        if tiempoParcial is not None:
            tiempoParcial = json.loads(tiempoParcial)
            # Do something with the tiempoParcial object here
        else:
            print("tiempoParcial is None")
    else:
        print("Request method is not POST")
    return JsonResponse({'status': 'success'})
    ...


def base(request):
    """
    Representa la plantilla base para la aplicación de cronómetro.

    Parámetros:
        solicitud (HttpRequest): el objeto de solicitud HTTP.

    Devoluciones:
        HttpResponse: la plantilla base renderizada.
    """
    return render(request,'cronometro/base/base.html')

def crearOperario(request):
    """
    Crea un operario utilizando el objeto de solicitud y presenta la plantilla form_operario.html.

    :param request: el objeto de solicitud HTTP que contiene información sobre la solicitud del usuario
    :tipo de solicitud: HttpRequest
    :return: un objeto de respuesta HTML que representa la plantilla form_operario.html
    :rtype: HttpRespuesta
    """
    return render((request), 'cronometro/operario/form_operario.html')


def guardarOperario (request):
    """
    Guarda un operario en la base de datos.
    Parameters:
    request (HttpRequest): La solicitud HTTP recibida.
    Returns:
        HttpResponseRedirect: Redirige al usuario hacia la página home si el operario se guarda correctamente.
    """
    
    try: 
        if request.method == "POST":
            operario = Operario(
                email= request.POST['email'],
                nombre= request.POST['nombre'],
                entidad= request.POST['entidad'],
                estado= request.POST['estado'],
                #fecha= request.POST['email'],
                #factorRitmo= request.POST['email'],
                #tiempoEstandar= request.POST['email'],
                #escalaSuplementos= request.POST['email'],
                
            )
            operario.full_clean()
            operario.save()
            messages.success(request, f"Operari@ ha sido creado con éxito")
        
        else:
            messages.warning(request, "Usted no ha enviado datos")
    
    except Exception as e:
        messages.error(request, f"Error: Ya existe un usuario con este correo")
        return redirect('cronometro:crearOperario')
        
    return redirect('cronometro:home')  

def listarOperarios(request):
    """
    Listar Operarios.
    Esta función enumera los operarios (trabajadores). Comprueba si el usuario ha iniciado sesión y, de ser así, recupera una lista de operarios de la base de datos, pagina los resultados y renderiza la plantilla 'cronometro/operario/listado_operarios.html' con los datos de los operarios. Si el usuario no ha iniciado sesión, muestra un mensaje de advertencia y redirige a la URL 'cronometro:home'.


    Parámetros
    ----------
    solicitud: Solicitud Http
        El objeto de solicitud HTTP.

    Devoluciones
    -------
    Respuesta HTTP
        La respuesta HTTP que contiene la plantilla representada o una respuesta de redireccionamiento.

     """
    login = request.session.get('logueoUsuario', False)
    if login:
        operarios = Operario.objects.order_by('-estado')
        paginator = Paginator(operarios, 10)
        page_number = request.GET.get('page')
        operarios = paginator.get_page(page_number)
        return render(request, 'cronometro/operario/listado_operarios.html', {'operarios' : operarios})
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('cronometro:home')

def actualizarOperario(request, id):
    """
    Actualiza la información de un operador y devuelve la página HTML correspondiente para editarla.

    Parámetros:
        solicitud (HttpRequest): el objeto de solicitud HTTP.
        id (int): El ID del operador que se actualizará.

    Devoluciones:
        HttpResponse: la página HTML para editar la información del operador.


     """
    login = request.session.get('logueoUsuario', False)
    if login:
        if login:
            operario = Operario.objects.get(id = id)
            return render(request, 'cronometro/operario/edicion_operario.html', {'operario': operario})
        else:
            messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('cronometro:listarOperarios')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('cronometro:home')

def edicionOperario(request):
    """
    Edita un operador según la solicitud proporcionada.

    Argumentos:
        solicitud (HttpRequest): el objeto de solicitud HTTP que contiene la información necesaria.
    
    Devoluciones:
        HttpResponseRedirect: Redirige a la vista 'listarOperarios' luego de editar el operador.
    

    """
    try:
        login = request.session.get('logueoUsuario', False)
        if login:
            if login:
                if request.method == "POST":
                    operario = Operario.objects.get(id = request.POST['id'])
                    
                    operario.nombre = request.POST['nombre']
                    operario.entidad = request.POST['entidad']
                    operario.estado = request.POST['estado']
                    
                    operario.save()
                    messages.success(request, f"operario ({operario.nombre})  editado exitosamente")
                else:
                    messages.warning(request, "Usted no ha enviado datos")
            else:
                messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
                return redirect('cronometro:listarOperarios')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarOperarios')

def deshabilitarOperario(request, id):
    """
    Desactiva un operador.

    Argumentos:
        solicitud: el objeto de la solicitud.
        id: El ID del operador a deshabilitar.

    Devoluciones:
        Una redirección a la vista 'listarOperarios'.


    """
    
    try:
        login = request.session.get('logueoUsuario', False)
        if login:
            operario = Operario.objects.get(id = id)
            if operario.estado == True:
                operario.estado = False
            else:
                operario.estado = True
            
            operario.save()
            messages.success(request, f"Proveedor ({operario.nombre}) deshabilitado exitosamente")
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarOperarios')

def guardarTiempoParcial(request):
    """
     Guarda el tiempo parcial de una solicitud.
    
     Parámetros:
         - solicitud: el objeto de solicitud HTTP.
        
     Devoluciones:
         - render: La respuesta HTTP renderizada con la plantilla 'cronometro\cronometro.html'.
     """
    
    try:
        #if request.method == "POST":
           # tiempoParcial = request.POST.get('tiempos_cookie')
           # if tiempoParcial is not None:
               # tiempoParcial = json.loads(tiempoParcial)

        if request.method == "POST":
            #tiempoEstandar = request.session.get('tiempos_estandar')
            idOperario = request.POST['idOperario']
            operario = Operario.objects.get(id = idOperario)
            
            operario.factorRitmo= request.POST['factorRitmo']
            operario.escalaSuplementos= request.POST['escalaSuplementos']
            #operario.tiempoEstandar = tiempoEstandar
            operario.save()
                    
            messages.success(request, f"Operario ({operario.nombre}) seleccionado con éxito")
           # else:
                #print("tiempos cookie es None")
        else:
            print("El metodo de solisitud no es POST")
        #return JsonResponse({'status': 'success'})
            
    except Exception as e:
        messages.warning(request, f"Error: {e}")
        
    return render(request,'cronometro\cronometro.html',{'operario' : operario})


# Maquina
def crearMaquina(request):
    
    return render((request), 'cronometro/maquina/registro_maquina.html')

def guardarMaquina(request):
    try: 
        if request.method == "POST":
            maquina = Maquina(
                nombre= request.POST['nombre'],
                descripcion= request.POST['descripcion'],
                estado= True
                 
            )
            maquina.full_clean()
            maquina.save()
            messages.success(request, f"maquina ha sido creado con éxito")
        
        else:
            messages.warning(request, "Usted no ha enviado datos")
    
    except Exception as e:
        messages.error(request, f"Error: Ya existe un elemento con estos datos")
        return redirect('cronometro:crearMaquina')
        
    return redirect('cronometro:home') 

def listarMaquinas(request):
    
    login = request.session.get('logueoUsuario', False)
    if login:
        maquinas= Maquina.objects.order_by('-estado')
        paginator = Paginator(maquinas, 10)
        page_number = request.GET.get('page')
        maquinas = paginator.get_page(page_number)
        return render(request, 'cronometro/maquina/listado_maquinas.html', {'maquinas' : maquinas})
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('cronometro:home')

def deshabilitarMaquina(request, id):
    try:
        login = request.session.get('logueoUsuario', False)
        if login:
            maquina = Maquina.objects.get(id = id)
            if maquina.estado == True:
                maquina.estado = False
            else:
                maquina.estado = True
            
            maquina.save()
            messages.success(request, f"Estado Maquina ({maquina.nombre}) cambiado exitosamente")
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarMaquinas')
def actualizarMaquina(request, id):
    login = request.session.get('logueoUsuario', False)
    if login:
        if login:
            maquina = Maquina.objects.get(id = id)
            return render(request, 'cronometro/maquina/edicion_maquina.html', {'maquina': maquina})
        else:
            messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('cronometro:listarMaquinas')
    else:
        messages.warning(request, "Inicie sesión primero")
        return redirect('cronometro:home')

def editarMaquina(request):
    try:
        login = request.session.get('logueoUsuario', False)
        if login:
            if login:
                if request.method == "POST":
                    maquina = Maquina.objects.get(id = request.POST['id'])
                    
                    maquina.nombre = request.POST['nombre']
                    maquina.descripcion = request.POST['descripcion']
                    maquina.estado = request.POST['estado']
                    
                    maquina.save()
                    messages.success(request, f"maquina ({maquina.nombre})  editado exitosamente")
                else:
                    messages.warning(request, "Usted no ha enviado datos")
            else:
                messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
                return redirect('cronometro:listarMaquinas')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarMaquinas')



def guardarTiempoEstandar(request, id):
    """
    Guarda el tiempo estándar de un operador en la base de datos y muestra un mensaje de éxito.

    Argumentos:
        solicitud (HttpRequest): el objeto de solicitud HTTP.
        id (int): El ID del operador.
    
    Devoluciones:
        HttpResponse: el objeto de respuesta HTTP con la plantilla representada.
    """
    try:
        tiempoE = 0
        operario = Operario.objects.get(id = id)
        #print(json.dumps(request.session.get('tiempos_cookie')))
        
        if 'tiempos_estandar' in request.COOKIES: #de esta forma ya que esta cookie esta en el navegador al ser creada con js
            tiempoE = request.COOKIES['tiempos_estandar']
            print(tiempoE)
            operario.tiempoEstandar= float( (tiempoE))
            operario.save()
        messages.success(request, f"Datos guardados ({(tiempoE)}) con éxito")
        return render(request,'cronometro/cronometro.html',{'operario' : operario})
    
    except Exception as e:
        messages.warning(request, f"Error: {e}")
    return render(request,'cronometro/cronometro.html',{'operario' : operario})
    #return redirect('cronometro:cronometro')
    


#Informe en excel

def generarInforme(request, id):
    """
    Genera un informe de Excel para un operario determinado y lo devuelve como un archivo descargable.

    Parámetros:
    - solicitud: el objeto de solicitud HTTP.
    - id: El ID del operario.

    Devoluciones:
    - respuesta: un objeto de respuesta HTTP que contiene el informe de Excel generado como un archivo descargable.
    """
    operario = Operario.objects.get(id = id)
    # Crear un libro de Excel
    libro = Workbook()
    hoja = libro.active

    # Agregar encabezados
    hoja['A1'] = 'Fecha'
    hoja['B1'] = 'Nombre'
    hoja['C1'] = 'Entidad'
    hoja['D1'] = 'Email'
    hoja['E1'] = 'Tiempo estandar' 
    hoja['F1'] = 'Factor de ritmo'
    hoja['G1'] = 'Escala suplementos'
    
    # Agregar datos
    hoja['A2'] = operario.fecha.astimezone(pytz.UTC).replace(tzinfo=None)
    hoja['B2'] = operario.nombre
    hoja['C2'] = operario.entidad
    hoja['D2'] = operario.email
    hoja['E2'] = operario.tiempoEstandar
    hoja['F2'] = operario.factorRitmo
    hoja['G2'] = operario.escalaSuplementos
    

    # Definir nombre del archivo
    nombre_archivo = 'informeOperario.xlsx'

    # Crear la respuesta HTTP con el archivo adjunto
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'

    # Guardar el libro de Excel en la respuesta HTTP
    libro.save(response)

    return response
