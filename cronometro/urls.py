from django.urls import path
from .views import *


urlpatterns = [
    path('', homeView, name='home'),
    path('cronometro', cronometroView, name='cronometro'),
]