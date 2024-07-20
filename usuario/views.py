from django.shortcuts import render, redirect, get_object_or_404
from django.db import Error
from django.template import loader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Usuario
from .forms import UsuarioForm
from django.contrib.auth.models import Group
import os

def register(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid ():
            form.save()
            return redirect('login')
    else:
        form = UsuarioForm()

    # Obtém o valor de 'tipo' do formulário, se presente
    tipo = request.POST.get('tipo', None)

    # Verifica se 'tipo' é válido e se não, define um valor padrão
    if tipo not in ['1', '2']:
        tipo = '1'  # Defina o valor padrão como '1' se não estiver definido

    return render(request, 'registration/register.html', {'form': form, 'tipo': tipo})

def usuario_ou_admin_master(u):
    return u.groups.filter(name__in=['Administrador de Setor', 'Administrador Master']).exists()

#metodo que lista todos os usuarios registrados
@login_required
@user_passes_test(usuario_ou_admin_master)
def listarUsuarios(request):
    search_query = request.GET.get('searchbar', '')  # pega o parâmetro de pesquisa
    if search_query:
        usuarios_list = Usuario.objects.filter(
            first_name__icontains=search_query
        ) | Usuario.objects.filter(
            last_name__icontains=search_query
        )
    else:
        usuarios_list = Usuario.objects.all()

    total_usuarios = usuarios_list.count()  # total de usuários registrados

    # Paginação
    paginator = Paginator(usuarios_list, 10)  # mostra apenas 10 usuários por página
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)

    return render(request, "partials/usuario/listarUsuarios.html", {
        'usuarios': usuarios,
        'total_usuarios': total_usuarios,
        'search_query': search_query
    })