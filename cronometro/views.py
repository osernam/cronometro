from django.shortcuts import render

# Create your views here.

def homeView(request):
    return render(request,'cronometro\index.html')

def cronometroView(request):
    return render(request,'cronometro\cronometro.html')