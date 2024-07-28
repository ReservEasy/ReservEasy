from django.urls import path
from . import views

urlpatterns = [
    path('reservar/', views.criar_reserva, name='registrar_reserva'),
    path('reservas/', views.listar_reservas, name='listar_reservas'),
]
