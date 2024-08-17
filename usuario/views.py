from django.shortcuts import render, redirect, get_object_or_404
from django.db import Error
from django.template import loader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Usuario
from .forms import UsuarioForm, UsuarioUpdateForm
from django.contrib.auth.models import Group
from django.contrib import messages
import os

def register(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid ():
            usuario = form.save() #salva o usuario e guarda as informações dele
            solicitante_group, created = Group.objects.get_or_create(name='solicitante') #pega o grupo solicitante
            usuario.groups.add(solicitante_group) #add o usuario ao grupo
            usuario.save() #salva as alterações
            # messages.success(request, "Usuário salvo com sucesso!")
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

@login_required
def perfilUser(request): #visualização do perfil do usuario
    usuario = get_object_or_404(Usuario, username=request.user.username) #busca o objeto Usuario correspondente ao usuário atualmente autenticado
    return render(request, 'partials/usuario/myprofile.html', {'usuario': usuario})

@login_required
def editarPerfilUser(request):
    usuario = get_object_or_404(Usuario, username=request.user.username)
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario, user=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario') 
    else:
        form = UsuarioUpdateForm(instance=usuario, user=usuario)
    return render(request, 'partials/usuario/myprofile_update.html', {'form': form, 'usuario': usuario})


@login_required
@user_passes_test(usuario_ou_admin_master)
def detalharUsuario(request, matricula):
    
    usuario = get_object_or_404(Usuario, matricula=matricula)
    reservas = usuario.reservas.all()   
    
    paginator = Paginator(reservas, 5)  # Mostra 5 reservas por página
    page_number = request.GET.get('page')  # obtém o número da página da URL
    page_obj = paginator.get_page(page_number)

    return render(request, 'partials/usuario/detalharUsuario.html', {
        'usuario': usuario,
        'reservas': page_obj,
    })    
@login_required
def promoverAdmMaster(request):

    return render(request, 'partials/usuario/promoverAdmMaster.html')

@login_required
def formAdmMaster(request):
    
    return render(request, 'partials/usuario/formAdmMaster.html')