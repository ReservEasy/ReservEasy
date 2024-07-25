from django.shortcuts import render, redirect, get_object_or_404
from django.db import Error
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Setor
from .forms import SetorForm
from django.contrib.auth.models import Group
import os

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def criarSetor(request):
    if request.method == 'POST':
        form = SetorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/setor/?msg=Salvo')
    else:
        form = SetorForm() #se tiver erro as informações do formulário voltam 
    return render(request, 'partials/setor/formSetor.html', {'form': form})

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def listarSetores(request):
    setores = Setor.objects.all()
    return render(request, "partials/setor/listarSetores.html", {'setores': setores})

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def editarSetor(request, id_setor):
    setor = Setor.objects.get(pk=id_setor)
    if request.method == 'POST':
        form = SetorForm(request.POST, instance= setor)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/setor/?msg=Salvo')
    else:
        form = SetorForm(instance= setor)
    return render(request, 'partials/setor/editarSetor.html', {'form':form, 'id_setor': id_setor})

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def deletar(request, id_setor):
    Setor.objects.get(pk=id_setor).delete()

    return HttpResponseRedirect("/setor/?msg=Exclui")

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm masterb
def confirmarDelete(request, id_setor):
    setor = Setor.objects.get(pk=id_setor)

    return render (request, 'partials/setor/confirmaExcluirSetor.html', {'setor':setor})
