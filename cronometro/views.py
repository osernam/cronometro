from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.db.models import Q
# Mensajes tipo cookies temporales
from django.contrib import messages

# Gestión de errores de base de datos
from django.db import IntegrityError    



# Create your views here.

def homeView(request):
    return render(request,'cronometro\index.html')

def cronometroView(request):
    return render(request,'cronometro\cronometro.html')

def tiempo_parcial(request):
    tiempoParcial = request.POST.get('tiempoParcial')
    print(tiempoParcial) # Output: 'tiempoParcial'
    
    return JsonResponse({'status': 'success'})
    ...


def base(request):
    return render(request,'cronometro/base/base.html')

def crearOperario(request):
    return render((request), 'cronometro/operario/form_operario.html')

def guardarOperario (request):
    
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