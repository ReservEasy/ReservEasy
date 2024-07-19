
from django.shortcuts import render, redirect, get_object_or_404
from django.db import Error
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Equipamento, Espaco
from .forms import EquipamentoForm, EspacoForm
from django.contrib.auth.models import Group
import os

# from braces.views import GroupRequiredMixin


# def index(request):
#     return HttpResponse("Hello, world. You're at the recurso index.")

@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def criarEquipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/recursos/?msg=Salvo')
    else:
        form = EquipamentoForm()
    return render(request, 'partials/recurso/formEquipamento.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def criarEspaco(request):
    if request.method == 'POST':
        form = EspacoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/recursos/?msg=Salvo')
    else:
        form = EspacoForm()
    return render(request, 'partials/recurso/formEspaco.html', {'form': form})


#metodo que lista todos os registros
@login_required
def listarRecursos(request):
    user = request.user #armazena qual usuário realizou a solicitação de listagem
    administrador_setor = Group.objects.get(name='Administrador de Setor') #obtem o grupo administrador de setor no bd
    is_admin_setor = administrador_setor in user.groups.all() #verifica se o grupo obtido está presente entre os grupos no qual o usuário atual pertence


    user.groups.set(administrador_setor)

    equipamentos = Equipamento.objects.all()
    espacos = Espaco.objects.all()
    recursos = list(equipamentos) + list(espacos)
    return render(request, "partials/recurso/listarRecursos.html", {'recursos': recursos, 'is_admin_setor': is_admin_setor})


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def editarRecurso(request, id_recurso):
    try:
        recurso = Equipamento.objects.get(pk=id_recurso)
        form_class = EquipamentoForm
    except Equipamento.DoesNotExist:
        recurso = get_object_or_404(Espaco, pk=id_recurso)
        form_class = EspacoForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=recurso)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/recursos/?msg=Salvo')
    else:
        form = form_class(instance=recurso)
    
    return render(request, 'partials/recurso/editarRecurso.html', {'form': form, 'id_recurso': id_recurso})


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def confirmarDeleteEquipamento(request, id_recurso):
    recurso = get_object_or_404(Equipamento, pk=id_recurso)
    return render(request, 'partials/recurso/confirmaExcluirEquipamento.html', {'recurso': recurso})


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def deletarEquipamento(request, id_recurso):
    equipamento = get_object_or_404(Equipamento, pk=id_recurso)
    
    # Verifica se o espaço possui uma imagem associada e exclui a imagem
    if equipamento.imagem:
        caminho_imagem = equipamento.imagem.path
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)
    
    # Exclui o espaço do banco de dados
    equipamento.delete()
    
    return HttpResponseRedirect("/recursos/?msg=Excluído")


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def confirmarDeleteEspaco(request, id_recurso):
    recurso = get_object_or_404(Espaco, pk=id_recurso)
    return render(request, 'partials/recurso/confirmaExcluirEspaco.html', {'recurso': recurso})


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def deletarEspaco(request, id_recurso):
    espaco = get_object_or_404(Espaco, pk=id_recurso)
    
    # Verifica se o espaço possui uma imagem associada e exclui a imagem
    if espaco.imagem:
        caminho_imagem = espaco.imagem.path
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)
    
    # Exclui o espaço do banco de dados
    espaco.delete()
    
    return HttpResponseRedirect("/recursos/?msg=Excluído")

    