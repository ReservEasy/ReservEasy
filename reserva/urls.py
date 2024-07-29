from django.urls import path
from . import views

urlpatterns = [
    path('reservar/', views.criar_reserva, name='registrar_reserva'),
    path('reservas/', views.listar_reservas, name='listar_reservas'),
    path('historico/', views.historicoSolicitacao, name='historico_solicitacoes'),
    path('reservar/enviada/<int:reserva_id>', views.solicitacaoEnviada, name='solicitacao_enviada'),
]
