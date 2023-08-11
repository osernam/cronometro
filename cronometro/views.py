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
    return render(request,'cronometro\index.html')

def selecOperario (request):
    operarios = Operario.objects.all()
    
    datos = [0, 59, 75, 20, 20, 55, 40]  
    datos_json = json.dumps(list(datos), cls=DjangoJSONEncoder)
    return render(request, 'cronometro\operario\selec_operario.html', {
        'datos_json': datos_json,
        'operarios' : operarios
    })
    
    
    return render(request,'cronometro\operario\selec_operario.html', {'operarios' : operarios})


def login (request):
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
    renderiza el template  

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

def logout(request):
    del request.session['logueoUsuario']
    return redirect('cronometro:home')
    
def cronometroView(request):
    operarios = Operario.objects.all()
    return render(request,'cronometro\cronometro.html', {'operarios' : operarios})

def tiempo_parcial(request):
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

def guardarTiempoParcial(request):
    
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

def guardarTiempoEstandar(request, id):
    try:
        tiempoEstandar = 'sin datos'
        operario = Operario.objects.get(id = id)
        #print(json.dumps(request.session.get('tiempos_cookie')))
        
        if 'tiempos_estandar' in request.COOKIES: #de esta forma ya que esta cookie esta en el navegador al ser creada con js
            tiempoEstandar = request.COOKIES['tiempos_estandar']
            operario.tiempoEstandar= float(tiempoEstandar)
            operario.save()
        messages.success(request, f"Datos guardados ({tiempoEstandar}) seleccionado con éxito")
        return render(request,'cronometro/cronometro.html',{'operario' : operario})
    
    except Exception as e:
        messages.warning(request, f"Error: {e}")
    return render(request,'cronometro/cronometro.html',{'operario' : operario})
    #return redirect('cronometro:cronometro')
    
#grafico

def stats(request):
    views = (
        View.objects.all()	    
        .annotate(date=TruncDay("created_at"))
        .values("date")
        .annotate(y=Count("id"))
        .order_by("-date")
    )    
    view_s = json.dumps(list(views), cls=DjangoJSONEncoder)
    return render(request, 'stats.html', {
        'view_s': view_s,
    })

def actualizarDatos(request):
    # Obtén los nuevos datos del gráfico
    nuevos_datos = random.randint(0, 100)

    # Devuelve los nuevos datos en formato JSON
    return JsonResponse(nuevos_datos, safe=False)