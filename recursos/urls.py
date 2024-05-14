from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("create/", views.criar, name="criar"),
    path("", views.listarRecursos, name="listar"), #padrão ir pra cá, padrão listar
    path("editar/<int:id_recurso>", views.editar, name="editar"),
    path("deletar/<int:id_recurso>", views.deletar, name="deletar"), 
    path("deletar/confirmar/<int:id_recurso>", views.confirmarDelete, name="confirmar"), 
    path("detalhar/<int:id_recurso>", views.detail, name="detalhar"), 
    #<int:id_cidade> == padrão de como será

]