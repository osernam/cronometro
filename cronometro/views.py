from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


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