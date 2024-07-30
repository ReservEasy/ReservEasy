from django.urls import path

from . import views

urlpatterns = [
    path("createEquipamento/", views.criarEquipamento, name="criarEquipamento"),
    path("createEspaco/", views.criarEspaco, name="criarEspaco"),
    path("estoque", views.listarRecursos, name="listarRecursos"), #padrão ir pra cá, padrão listar
    path('editar/<int:id_recurso>/', views.editarRecurso, name='editarRecurso'),
    path("deletarEquipamento/<int:id_recurso>", views.deletarEquipamento, name="deletarEquipamento"), 
    path("deletarEspaco/<int:id_recurso>", views.deletarEspaco, name="deletarEspaco"), 
    path("deletarEquipamento/confirmar/<int:id_recurso>", views.confirmarDeleteEquipamento, name="confirmarDeleteEquipamento"), 
    path("deletarEspaco/confirmar/<int:id_recurso>", views.confirmarDeleteEspaco, name="confirmarDeleteEspaco"), 

]