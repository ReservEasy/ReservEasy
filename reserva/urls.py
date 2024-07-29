from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_reservas_usuario, name="listar_reservas_usuario"), #padrão ir pra cá, padrão listar
    path('reservar/', views.criar_reserva, name='registrar_reserva'),
    path("detalhar/<int:id_reserva>", views.detalharReserva, name="detalharReserva"),
    path("deletar/<int:id_reserva>", views.deletarReserva, name="deletarReserva"),
    path('historico/', views.historicoSolicitacao, name='historico_solicitacoes'),
    path('reservar/enviada/<int:reserva_id>', views.solicitacaoEnviada, name='solicitacao_enviada'),
    # path('solicitacoes', view.solicitacoespendentes, name='solicitacoespendentes'),
]
