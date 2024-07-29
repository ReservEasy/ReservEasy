from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_reservas_usuario, name="listar_reservas_usuario"), #padrão ir pra cá, padrão listar
    path('reservar/', views.criar_reserva, name='registrar_reserva'),
    path('reservas/', views.listar_reservas, name='listar_reservas'),
    path("detalhar/<int:id_reserva>", views.detalharReserva, name="detalharReserva"),
    path("deletar/<int:id_reserva>", views.deletarReserva, name="deletarReserva"),
]
