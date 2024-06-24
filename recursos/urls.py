from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("createEquipamento/", views.criarEquipamento, name="criarEquipamento"),
    path("createEspaco/", views.criarEspaco, name="criarEspaco"),
    path("", views.listarRecursos, name="listar"), #padrão ir pra cá, padrão listar
    path('editar/<int:id_recurso>/', views.editarRecurso, name='editarRecurso'),
    path("deletar/<int:id_recurso>", views.deletar, name="deletar"), 
    path("deletarEquipamento/confirmar/<int:id_recurso>", views.confirmarDeleteEquipamento, name="confirmarDeleteEquipamento"), 
    path("deletarEspaco/confirmar/<int:id_recurso>", views.confirmarDeleteEspaco, name="confirmarDeleteEspaco"), 
    path("detalhar/<int:id_recurso>", views.detail, name="detalhar"), 
    #<int:id_cidade> == padrão de como será

]