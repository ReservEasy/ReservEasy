from django.urls import path
from . import views

urlpatterns = [
    path("painel", views.acessarDashboard, name="acessar_paineldecontrol"),
    path("listar", views.listar_reservas_usuario, name="listar_reservas_usuario"), #padrão ir pra cá, padrão listar
    path('reservar/', views.criar_reserva, name='registrar_reserva'),
    path("detalhar/<int:id_reserva>", views.detalharReserva, name="detalharReserva"),
    path("deletar/<int:id_reserva>", views.deletarReserva, name="deletarReserva"),
    path('historico/', views.historicoSolicitacao, name='historico_solicitacoes'),
    path('reservar/enviada/<int:reserva_id>', views.solicitacaoEnviada, name='solicitacao_enviada'),
    path('solicitacoes/analise/', views.solicitacoes, name='solicitacoes'),
    path('solicitacoes/<int:reserva_id>/atualizar_status/<str:status>/', views.atualizar_status_reserva, name='atualizar_status_reserva'),
    path('reservas/pendencias/', views.reservasPendentes, name='reservasPendentes'),
    path('reservas/<int:reserva_id>/atualizar_situacao/<str:situacao>/', views.atualizar_situacao_reserva, name='atualizar_situacao_reserva' )
]
