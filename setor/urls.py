from django.urls import path

from . import views

urlpatterns = [
    path("", views.listarSetores, name="listar"), #padrão ir pra cá, padrão listar
    path("criarSetor/", views.criarSetor, name="criarSetor"),
    path("detalhar/<int:id_setor>", views.detalharSetor, name="detalharSetor"),
    path("alocarAdm/<int:id_setor>", views.alocarAdm, name="alocarAdm"),
    path("removerAdm/<int:id_adm>", views.removerAdm, name="removerAdm"),
    path("transferirAdm/<int:id_adm>", views.transferirAdm, name="transferirAdm"),
    path('editar/<int:id_setor>/', views.editarSetor, name='editarSetor'),
    path("deletar/<int:id_setor>", views.deletar, name="deletarSetor"),
    path("deletar/confirmar/<int:id_setor>", views.confirmarDelete, name="confirmarDeleteSetor"), 
]