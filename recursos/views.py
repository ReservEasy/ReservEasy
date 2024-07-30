
from django.shortcuts import render, redirect, get_object_or_404
from django.db import Error
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Equipamento, Espaco
from usuario.models import Usuario
from .forms import EquipamentoForm, EspacoForm
from django.contrib.auth.models import Group
import os
from django.core.paginator import Paginator

@login_required
def index(request):
    oi = "oi"

def usuario_ou_admin_master(u):
    return u.groups.filter(name__in=['Administrador de Setor', 'Administrador Master']).exists()

@user_passes_test(usuario_ou_admin_master)
def listarRecursos(request):
    user = request.user #armazena qual usuário realizou a solicitação de listagem
    search_query = request.GET.get('searchbar', '')  # pega o parâmetro de pesquisa
    if search_query:
        equipamentos = Equipamento.objects.filter(nome__icontains=search_query)
        espacos = Espaco.objects.filter(nome__icontains=search_query)
    else:
        equipamentos = Equipamento.objects.all()
        espacos = Espaco.objects.all()
    
    recursos = list(equipamentos) + list(espacos)
    usuario = Usuario.objects.get(pk=user.id)
    total_recursos = len(recursos)

    recursos_mesmo_setor = recursos
    tipo_adm = "Adm Master"
    if request.user.groups.filter(name="Administrador Master").exists():
        tipo_adm = "Adm Master"
    elif request.user.groups.filter(name="Administrador de Setor").exists():
        tipo_adm = "Adm Setor"
        recursos_mesmo_setor = [recurso for recurso in recursos if recurso.setor == usuario.setor]
        total_recursos = len(recursos_mesmo_setor)

    # paginação
    paginator = Paginator(recursos_mesmo_setor, 5) # Mostra 7 recursos por página
    page_number = request.GET.get('page')
    recursos_page = paginator.get_page(page_number)
    

    return render(request, "partials/recurso/listarRecursos.html", {
        'recursos': recursos_page,
        'total_recursos': total_recursos,
        'tipo_adm': tipo_adm,
        'usuario': usuario,
        'search_query': search_query
    })


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def criarEquipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, request.FILES)
        if form.is_valid():
            equipamento = form.save(commit=False)
            equipamento.setor = request.user.usuario.setor  # Define o setor do recurso com base no setor do usuário
            equipamento.save()
            return HttpResponseRedirect('/recursos/?msg=Salvo')
    else:
        form = EquipamentoForm()
    return render(request, 'partials/recurso/formEquipamento.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def criarEspaco(request):
    if request.method == 'POST':
        form = EspacoForm(request.POST, request.FILES)
        if form.is_valid():
            espaco = form.save(commit=False)
            espaco.setor = request.user.usuario.setor  # Define o setor do recurso com base no setor do usuário
            espaco.save()
            return HttpResponseRedirect('/recursos/?msg=Salvo')
    else:
        form = EspacoForm()
    return render(request, 'partials/recurso/formEspaco.html', {'form': form})


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

# @login_required
# def tipoAdm(request):
#     adm = "Solicitante"
#     if request.user.is_authenticated:
#         if request.user.groups.filter(name="Administrador Master").exists():
#             adm = "Adm Master"
#         elif request.user.groups.filter(name="Administrador de Setor").exists():
#             adm = "Adm Setor"
#     return render(request, '_sidebar.html', {'adm': adm})
    