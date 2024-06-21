
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


def index(request):
    return HttpResponse("Hello, world. You're at the recurso index.")

# @user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
# def criar(request):
#     if request.method == 'POST':
#         form = RecursoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/recursos/?msg=Salvo')
#     else:
#         form = RecursoForm()
#     return render(request, 'partials/recurso/formRecurso.html', {'form':form})

def criarEquipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/recursos/?msg=Salvo')
    else:
        form = EquipamentoForm()
    return render(request, 'partials/recurso/formEquipamento.html', {'form': form})

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
    user = request.user
    administrador_setor = Group.objects.get(name='Administrador de Setor')
    is_admin_setor = administrador_setor in user.groups.all()

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
def deletar(request, id_recurso):
    try:
        equipamento = Equipamento.objects.get(pk=id_recurso)
        recurso = equipamento
    except Equipamento.DoesNotExist:
        equipamento = None

    if equipamento is None:
        try:
            espaco = Espaco.objects.get(pk=id_recurso)
            recurso = espaco
        except Espaco.DoesNotExist:
            espaco = None

    if recurso is None:
        return HttpResponseRedirect("/recursos/?msg=Recurso não encontrado")

    if recurso.imagem:
        caminho_imagem = recurso.imagem.path
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)

    recurso.delete()

    return HttpResponseRedirect("/recursos/?msg=Excluído")


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists()) 
def confirmarDelete(request, id_recurso):
    try:
        equipamento = Equipamento.objects.get(pk=id_recurso)
        recurso = equipamento
    except Equipamento.DoesNotExist:
        equipamento = None

    if equipamento is None:
        try:
            espaco = Espaco.objects.get(pk=id_recurso)
            recurso = espaco
        except Espaco.DoesNotExist:
            espaco = None

    if recurso is None:
        return HttpResponseRedirect("/recursos/?msg=Recurso não encontrado")

    return render(request, 'partials/recurso/confirmaExcluir.html', {'recurso': recurso})

@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def detail(request, id_recurso):
    ##saida = recurso.objects.get(pk = id_recurso)
    ##template = loader.get_template("recurso/index.html")
    ##return HttpResponse(template.render({'recurso': saida}, request))

    try:
        saida = Recurso.objects.get(pk=id_recurso)
    except:
        saida = "Não há esse recurso (espaço ou equipamento)"
    
    return render(request, "recurso/index.html", {'recurso': saida})

    