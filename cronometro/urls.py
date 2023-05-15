from django.urls import path
from .views import *


urlpatterns = [
    path('index', homeView, name='home'),
    path('cronometro/', cronometroView, name='cronometro'),
    path('cronometro/tiempo-parcial/', tiempo_parcial, name='tiempo-parcial'),
    path('cronometro/base/', base, name='base'),
]