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
# recuperacion de contraseña
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404

from django.core.mail import send_mail
from django.conf import settings
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
    return render(request,'cronometro/index.html')

def homeView2(request):
    return render(request,'cronometro/base/base2.html')

def selecOperario (request):
    """
        Representa la plantilla 'selec_operario.html' con la solicitud dada.

        Parámetros:
            solicitud (HttpRequest): el objeto de solicitud HTTP.
        
        Devoluciones:
            HttpResponse: el objeto de respuesta HTTP.
        """
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
        
        
        operarios = Operario.objects.filter(estado=True)
        maquinas = Maquina.objects.filter(estado=True)
        operaciones = Operacion.objects.filter(estado=True)
        
        #datos_json = json.dumps(list(datos), cls=DjangoJSONEncoder)
        #return render(request, 'cronometro/operario/selec_operario.html', {
        #   'datos_json': datos_json,
        #  'operarios' : operarios
        #})
            
        return render(request,'cronometro/operario/selec_operario.html', {'operarios' : operarios , 'maquinas' : maquinas , 'operaciones' : operaciones})
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')

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
                password= contexto.hash(request.POST['clave']),
                username= request.POST['email'],
                estado=False
                
            )
            usuario.full_clean()
            usuario.save()
            messages.success(request, f"El usuario  ha sido creado con éxito")
        
        else:
            messages.warning(request, "Usted no ha enviado datos")
    
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect('cronometro:registro')
        
    return redirect('cronometro:home')  


def inicioRecuperacion(request):
    return render(request, 'cronometro/usuario/inicio_recuperacion.html')

def correoRecuperacion(request):
    try:    
        if request.method == "POST":
            
            correo=  request.POST['correo'],
            correoV=  request.POST['correoV'],
            print(correo)
            print(correoV)
            
            if correo== correoV:
                usuario= Usuario.objects.get(email = request.POST['correo'])
                print(usuario.nombre)
                email= usuario.email
                
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(usuario)
                # Almacena el token asociado con el usuario
                from django.contrib.sites.shortcuts import get_current_site

                request.session["usuarioR"] = [usuario.id]
                domain = get_current_site(request).domain
                mensaje = f'Haz clic en el siguiente enlace para restablecer tu contraseña: http://{domain}/cronometro/recuperar/?token={token}'
                #mensaje = f'Haz clic en el siguiente enlace para restablecer tu contraseña: http://127.0.0.1:8000/cronometro/recuperar/?token={token}'
                
                send_mail('Recuperación de contraseña', 
                          mensaje, 
                          settings.DEFAULT_FROM_EMAIL, 
                          [email],)
                
                messages.success(request, "Correo enviado")
                return redirect('cronometro:inicioRecuperacion')
            else:
                messages.warning(request, "Correo incorrecto")
                return redirect('cronometro:inicioRecuperacion')
        else:
            messages.warning(request, "Usted no ha enviado datos")
            return redirect('cronometro:inicioRecuperacion')
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect('cronometro:inicioRecuperacion')    
        
def recuperar(request):
    try:
        idUsuario = request.session.get('usuarioR')[0]
        
        print(idUsuario)
        token_generator = PasswordResetTokenGenerator()
        # Obtener el usuario correspondiente al token
        usuario = get_object_or_404(Usuario, pk=idUsuario)
        print(usuario)
        token = request.GET.get('token')
        print(token)

        # Validar el token
        if token_generator.check_token(usuario, token):
            # Token válido, permitir al usuario restablecer la contraseña
            # Mostrar un formulario para restablecer la contraseña
            messages.success(request, "Token válido")
            
            
            return render(request, 'cronometro/usuario/restablecer_contrasena.html', {'usuario': usuario})
        else:
            # Token inválido, mostrar un mensaje de error o redirigir a otra página
            # ...
            messages.warning(request, "Token inválido")
            return redirect('cronometro:inicioRecuperacion')
    except Usuario.DoesNotExist:
        # Handle the case when no Usuario object is found
        messages.warning(request, "Usuario no encontrado")
        return redirect('cronometro:inicioRecuperacion')
    
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect('cronometro:inicioRecuperacion')  

def formRestablecerContrasena(request, id):
    try:
        usuario = Usuario.objects.get(id = id)
        if request.method == "POST":
            
            clave = request.POST['password']
            claveV= request.POST['passwordV']
            
            if clave==claveV:
                usuario.clave = contexto.hash(clave)
                usuario.save()
                messages.success(request, "Contraseña actualizada")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return render(request, 'cronometro/usuario/restablecer_contrasena.html', {'usuario': usuario})
        
    

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
    if login[4] == 'Administrador':
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
    if Usuario.objects.get(id = login[0]).estado == True:
        if login:
            usuario = Usuario.objects.get(id = id)
            return render(request, 'cronometro/usuario/edicion_usuario.html', {'usuario': usuario})
        else:
            messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('cronometro:listarUsuarios')
    else:
        messages.warning(request, "Inicie sesión o solicite activar su cuenta")
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
                    
                    if usuario.email == "adm95193241@gmail.com":
                        usuario.rol = "A"
                        usuario.estado = True
                    else:
                        usuario.rol = request.POST['rol']
                        usuario.estado = request.POST['estado']
                        
                    usuario.save()
                    messages.success(request, f"Usuario ({usuario.nombre})  editado exitosamente")
                    return redirect('cronometro:home')
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
                if usuario.email == "adm95193241@gmail.com":
                    usuario.estado = True
                else:
                    usuario.estado = False
            else:
                usuario.estado = True
            
            
            
            usuario.save()
            
            messages.success(request, f"Proveedor ({usuario.nombre}) modificado exitosamente")
            
            return redirect('cronometro:listarUsuarios')
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
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
        operarios = Operario.objects.all()
        maquina = Maquina.objects.all()
        operacion = Operacion.objects.all()
        return render(request,'cronometro/cronometro.html', {'operarios' : operarios , 'maquina' : maquina, 'operacion' : operacion})
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')
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
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
        return render((request), 'cronometro/operario/form_operario.html')
    else:
        messages.warning(request, "Inicie sesión o solicite activar su cuenta")
        return redirect('cronometro:home')

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
            opExist= Operario.objects.filter(email= request.POST['email'])
            if opExist.exists():
                messages.warning(request, "Operari@ ya existe")
                return redirect('cronometro:crearOperario')
                
            else:
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
            return redirect('cronometro:home')
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
    try:
        login = request.session.get('logueoUsuario', False)
        if Usuario.objects.get(id = login[0]).estado == True:
            operarios = Operario.objects.order_by('-estado')
            paginator = Paginator(operarios, 10)
            page_number = request.GET.get('page')
            operarios = paginator.get_page(page_number)
            return render(request, 'cronometro/operario/listado_operarios.html', {'operarios' : operarios})
        else:
            messages.warning(request, "Inicie sesión o solicite activación")
            return redirect('cronometro:home')
    except Exception as e:
        messages.warning(request, "Inicie sesión o solicite activación")
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
    if Usuario.objects.get(id = login[0]).estado == True:
        if login:
            operario = Operario.objects.get(id = id)
            return render(request, 'cronometro/operario/edicion_operario.html', {'operario': operario})
        else:
            messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('cronometro:listarOperarios')
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
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
        if Usuario.objects.get(id = login[0]).estado == True:
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
            messages.warning(request, "Inicie sesión o solicite activación")
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
        if Usuario.objects.get(id = login[0]).estado == True:
            operario = Operario.objects.get(id = id)
            if operario.estado == True:
                operario.estado = False
            else:
                operario.estado = True
            
            operario.save()
            messages.success(request, f"Cambio de estado para ({operario.nombre}) exitoso")
        else:
            messages.warning(request, "Inicie sesión o solicite activación")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarOperarios')


def historial(request, id): 
    
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
        OperacionOperario.objects.filter(idOperario=id, tiempoEstandar=0).delete()
        historial = OperacionOperario.objects.filter(idOperario = id)
        operarios = Operario.objects.all()
        
        paginator = Paginator(historial, 10)
        page_number = request.GET.get('page')
        historial = paginator.get_page(page_number)
        return render(request, 'cronometro/operario/historico.html', {'historial' : historial})
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')

def eliminarHistoria(request, id):
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
        try:
            historial = OperacionOperario.objects.get(id = id)
            historial.delete()
            messages.success(request, f"Registro eliminado exitosamente")
            return redirect('cronometro:historial', id = historial.idOperario.id)
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('cronometro:historial', id = historial.idOperario.id)
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')
def guardarTiempoParcial(request):
    
    if request.method == "POST":
        #tiempoEstandar = request.session.get('tiempos_estandar')
        try:
            operario = Operario.objects.get(id = request.POST['idOperario'])
            operacion = Operacion.objects.get(id = request.POST['idOperacion'])
            maquina= Maquina.objects.get(id = request.POST['idMaquina'])
            
            ritmo= request.POST['factorRitmo']
            suplementos= request.POST['escalaSuplementos']
            
            ritmoP= ritmo.replace(",", ".")
            suplementosP= suplementos.replace(",", ".")
            
            
            opOpera= OperacionOperario(
                idOperario= operario,
                idOperacion= operacion,
                idMaquinas= maquina,
                factorRitmo= float(ritmoP),
                escalaSuplementos= float(suplementosP),
            )
            
            
            opOpera.save()
            print("guardado")
            messages.success(request, f"Datos seleccionados con éxito")
            return render(request,'cronometro/cronometro.html',{'operario' : operario , 'operacion' : operacion, 'maquina' : maquina , 'opOpera' : opOpera})
        except Exception as e:
            messages.warning(request, f"Error: {e} vacio")
            print( f"Error: {e}")
    else:
        return HttpResponse(request,"no se envio datos")
    #return HttpResponse(request,"OK")
    return redirect('cronometro:selecOperario')

# Maquina
def crearMaquina(request):
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
        
        return render((request), 'cronometro/maquina/registro_maquina.html')
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')

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
    if Usuario.objects.get(id = login[0]).estado == True:
        maquinas= Maquina.objects.order_by('-estado')
        paginator = Paginator(maquinas, 10)
        page_number = request.GET.get('page')
        maquinas = paginator.get_page(page_number)
        return render(request, 'cronometro/maquina/listado_maquinas.html', {'maquinas' : maquinas})
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')

def deshabilitarMaquina(request, id):
    try:
        login = request.session.get('logueoUsuario', False)
        if Usuario.objects.get(id = login[0]).estado == True:
            maquina = Maquina.objects.get(id = id)
            if maquina.estado == True:
                maquina.estado = False
            else:
                maquina.estado = True
            
            maquina.save()
            messages.success(request, f"Estado Maquina ({maquina.nombre}) cambiado exitosamente")
        else:
            messages.warning(request, "Inicie sesión o solicite activación")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarMaquinas')
def actualizarMaquina(request, id):
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
        if login:
            maquina = Maquina.objects.get(id = id)
            return render(request, 'cronometro/maquina/edicion_maquina.html', {'maquina': maquina})
        else:
            messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('cronometro:listarMaquinas')
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')

def editarMaquina(request):
    try:
        login = request.session.get('logueoUsuario', False)
        if Usuario.objects.get(id = login[0]).estado == True:
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
            messages.warning(request, "Inicie sesión o solicite activación")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarMaquinas')

# Operación
def crearOperacion(request):
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
        return render((request), 'cronometro/operacion/registro_operacion.html')
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')

def guardarOperacion(request):
    try: 
        if request.method == "POST":
            operacion = Operacion(
                nombre= request.POST['nombre'],
                descripcion= request.POST['descripcion'],
                estado= True
                 
            )
            operacion.full_clean()
            operacion.save()
            messages.success(request, f"operacion ha sido creado con éxito")
        
        else:
            messages.warning(request, "Usted no ha enviado datos")
    
    except Exception as e:
        messages.error(request, f"Error: Ya existe un elemento con estos datos")
        return redirect('cronometro:crearOperacion')
        
    return redirect('cronometro:home') 

def listarOperaciones(request):
    
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
        operaciones= Operacion.objects.order_by('-estado')
        paginator = Paginator(operaciones, 10)
        page_number = request.GET.get('page')
        operaciones = paginator.get_page(page_number)
        return render(request, 'cronometro/operacion/listado_operaciones.html', {'operaciones' : operaciones})
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')

def deshabilitarOperacion(request, id):
    try:
        login = request.session.get('logueoUsuario', False)
        if Usuario.objects.get(id = login[0]).estado == True:
            operacion = Operacion.objects.get(id = id)
            if operacion.estado == True:
                operacion.estado = False
            else:
                operacion.estado = True
            
            operacion.save()
            messages.success(request, f"Estado de operacion ({operacion.nombre}) cambiado exitosamente")
        else:
            messages.warning(request, "Inicie sesión o solicite activación")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarOperaciones')
def actualizarOperacion(request, id):
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
        if login:
            operacion = Operacion.objects.get(id = id)
            return render(request, 'cronometro/operacion/edicion_operacion.html', {'operacion': operacion})
        else:
            messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
            return redirect('cronometro:listarOperaciones')
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')

def editarOperacion(request):
    try:
        login = request.session.get('logueoUsuario', False)
        if Usuario.objects.get(id = login[0]).estado == True:
            if login:
                if request.method == "POST":
                    operacion = Operacion.objects.get(id = request.POST['id'])
                    
                    operacion.nombre = request.POST['nombre']
                    operacion.descripcion = request.POST['descripcion']
                    operacion.estado = request.POST['estado']
                    
                    operacion.save()
                    messages.success(request, f"operacion ({operacion.nombre})  editado exitosamente")
                else:
                    messages.warning(request, "Usted no ha enviado datos")
            else:
                messages.warning(request, "No posee los permisos para hacer esa acción. Contacte un administrador")
                return redirect('cronometro:listarOperaciones')
        else:
            messages.warning(request, "Inicie sesión o solicite activación")
            return redirect('cronometro:home')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarOperaciones')


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
        login = request.session.get('logueoUsuario', False)
        if login:
            tiempoE = 0
            opOpera = OperacionOperario.objects.get(id = id)
            operario= Operario.objects.get(id = opOpera.idOperario.id)
            maquina= Maquina.objects.get(id = opOpera.idMaquinas.id)
            operacion= Operacion.objects.get(id = opOpera.idOperacion.id)
            
            #print(json.dumps(request.session.get('tiempos_cookie')))
            try:
                print( request.COOKIES['tiempos_estandar'])
                
                if request.method =="POST":            
                    escalaSuplementos = ( request.POST['escalaSuplemento'])
                    factorRitmo = (request.POST['factoRitmo'])
                    tObservado=  (request.POST['cajaTiempoObservado'])
                    
                    escalaSuplementos = escalaSuplementos.replace(",", ".")
                    factorRitmo = factorRitmo.replace(",", ".")
                    tObservado = tObservado.replace(",", ".")
                    
                    try:
                        escala = float(escalaSuplementos)
                        ritmo = float(factorRitmo)
                        observado = float(tObservado)
                        print("observado")
                        print(observado)
                        
                        opOpera.factorRitmo = ritmo        
                        opOpera.escalaSuplementos = escala
                        print("escala")
                        print(escala)
                        print("ritmo")
                        print(ritmo)
                        tNormal= observado* ritmo/100
                        print(tNormal)
                        tEstandar = tNormal+(tNormal*escala)
                        tEstandar = round(tEstandar, 2)
                        print("TE")
                        print(tEstandar)
                        opOpera.tiempoEstandar = tEstandar
                        opOpera.uniHoras = 60/tEstandar*0.8
                        print("")
                        opOpera.save()
                    except Exception as e:
                           
                        messages.error(request, f"No ha enviado datos válidos" )
                        
                        
                    
                    
                messages.success(request, f"Tiempo estandar ({(tEstandar)}) guardado con éxito")
                print("guardado")
            except Exception as e:
                print ( f"Error: {e}")
        #return render(request,'cronometro/cronometro.html',{'operarios' : operarios , 'maquinas' : maquinas , 'operaciones' : operaciones})


            return render(request,'cronometro/cronometro.html',{'operario' : operario , 'maquina' : maquina , 'operacion' : operacion, 'opOpera' : opOpera})
        #return redirect('cronometro:cronometro')
        else:
            messages.warning(request, "Inicie sesión primero")
            return redirect('cronometro:home')
    except Exception as e:
        print ( f"Error: {e}")

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
    login = request.session.get('logueoUsuario', False)
    if Usuario.objects.get(id = login[0]).estado == True:
            
        operario= Operario.objects.get(id = id)
        historico = OperacionOperario.objects.filter(idOperario = id)
        # Crear un libro de Excel
        libro = Workbook()
        hoja = libro.active

        # Agregar encabezados
        hoja['A1'] = 'Fecha'
        hoja['B1'] = 'Nombre'
        hoja['C1'] = 'Entidad'
        hoja['D1'] = 'Email'
        hoja['E1'] = 'Operación' 
        hoja['F1'] = 'Desc operación'
        hoja['G1'] = 'Maquina'
        hoja['H1'] = 'Desc Maquina' 
        hoja['I1'] = 'Suplementos'
        hoja['J1'] = 'Ritmo'
        hoja['K1'] = 'T estandar'
        hoja['L1'] = 'Uni/hora'
        
        # Agregar datos
        
        for i, registro in enumerate( historico, start=2):
            hoja[f'A{i}'] = registro.fechas.astimezone(pytz.UTC).replace(tzinfo=None)
            hoja[f'B{i}'] = registro.idOperario.nombre
            hoja[f'C{i}'] = registro.idOperario.entidad
            hoja[f'D{i}'] = registro.idOperario.email
            hoja[f'E{i}'] = registro.idOperacion.nombre
            hoja[f'F{i}'] = registro.idOperacion.descripcion
            hoja[f'G{i}'] = registro.idMaquinas.nombre
            hoja[f'H{i}'] = registro.idMaquinas.descripcion
            hoja[f'I{i}'] = registro.escalaSuplementos
            hoja[f'J{i}'] = registro.factorRitmo
            hoja[f'K{i}'] = registro.tiempoEstandar
            hoja[f'L{i}'] = registro.uniHoras
        

        # Definir nombre del archivo
        nombre_archivo = 'informe+' + (operario.nombre) + '.xlsx'

        # Crear la respuesta HTTP con el archivo adjunto
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'

        # Guardar el libro de Excel en la respuesta HTTP
        libro.save(response)

        return response
    else:
        messages.warning(request, "Inicie sesión o solicite activación")
        return redirect('cronometro:home')

def buscarOperario(request):
    try:
        login = request.session.get('logueoUsuario', False)
        if Usuario.objects.get(id = login[0]).estado == True:
            
            if request.method == "POST":
                resultado = request.POST["buscar"]
                
                operarios = Operario.objects.filter(Q(nombre__icontains = resultado) | Q(entidad__icontains = resultado) | Q(email__icontains = resultado) | Q(estado__icontains = resultado))
                paginator = Paginator(operarios, 10)
                page_number = request.GET.get('page')
                operarios = paginator.get_page(page_number)
                
                return render(request, 'cronometro/operario/listado_operarios.html', {'operarios' : operarios})
            else:
                messages.error(request, "No envió datos")
                return redirect('cronometro:listarOperarios')
        else:
            messages.warning(request, "Inicie sesión o solicite activación")
            return redirect('cronometro:listarOperarios')
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('cronometro:listarOperarios')



def redireccionar_a_inicio(request):
    return redirect('cronometro:home')
