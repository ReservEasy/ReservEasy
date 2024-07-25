from django.urls import path

from . import views

urlpatterns = [
    path("criarSetor/", views.criarSetor, name="criarSetor"),
    path("", views.listarSetores, name="listar"), #padrão ir pra cá, padrão listar
    path('editar/<int:id_setor>/', views.editarSetor, name='editarSetor'),
    path("deletar/<int:id_setor>", views.deletar, name="deletarSetor"),
    path("deletar/confirmar/<int:id_setor>", views.confirmarDelete, name="confirmarDeleteSetor"), 
]