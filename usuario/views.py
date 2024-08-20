from django.shortcuts import render, redirect, get_object_or_404
from django.db import Error
from django.template import loader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Usuario
from .forms import UsuarioForm, UsuarioUpdateForm, promoverAdm
from django.contrib.auth.models import Group
from django.contrib import messages
import os
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url  
from django.contrib.auth.views import LoginView as BaseLoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache 
from django.conf import settings


def register(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid ():
            usuario = form.save(commit=False) #guarda as informações do usuario, mas ainda não salva (pra alterar algumas coisas antes)
            tipo = request.POST.get('tipo') #pega o valor do campo tipo recebido e armazena na variavel tipo
            if tipo: #se tipo existir...
                usuario.tipo = tipo #o valor da variavel tipo é atribuido ao atributo tipo do usuario
            usuario = form.save() #salva o usuario e guarda as informações dele
            solicitante_group, created = Group.objects.get_or_create(name='Solicitante') #pega o grupo solicitante
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

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def listarAdmMaster(request):
    grupo_adm_master = Group.objects.get(name="Administrador Master")
    # Pega os IDs dos usuários do grupo
    usuarios_ids = grupo_adm_master.user_set.values_list('id', flat=True)
    # Conta o número de usuários no grupo
    total_adms_master = grupo_adm_master.user_set.count()
    # Verifica os usuários do model Usuario que têm o ID entre os selecionados acima
    adms_master = Usuario.objects.filter(id__in=usuarios_ids)
    return render(request, 'partials/usuario/listarAdmMaster.html', {
        'adms_master': adms_master,
        'total_adms_master': total_adms_master
    })

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def removerAdmMaster(request, id_adm):
    usuario = Usuario.objects.get(id=id_adm)
    group, created = Group.objects.get_or_create(name='Solicitante')  # Obtém ou cria o grupo
    usuario.groups.set([group])  # Define o grupo do usuário como o grupo 'Solicitante' (remove qualquer outro que tinha antes)
    usuario.save()
    return redirect(reverse('listarAdmMaster'))

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
@login_required
def promoverAdmMaster(request):
    if request.method == 'POST': #se receber um formulario
        form = promoverAdm(request.POST) #armazena o que obteve pelo form
        if form.is_valid():
            usuarios = form.cleaned_data['usuarios'] #pega a lista dos usuarios selecionados
            for usuario in usuarios: #for para definir o grupo dos usuarios como admMaster
                group, created = Group.objects.get_or_create(name='Administrador Master')  # Obtém ou cria o grupo
                usuario.groups.set([group])  # Define o grupo do usuário como o grupo 'Administrador Master' (remove qualquer outro que tinha antes)
                usuario.save()
            return redirect(reverse('listarAdmMaster'))
    else:
        grupo_adm_master = Group.objects.get(name="Administrador Master")
        # pega IDs dos usuários desse grupo
        usuarios_ids = grupo_adm_master.user_set.values_list('id', flat=True)
        # pega todos os usuários, com exceção dos que pertencem ao grupo "Administrador Master"
        usuarios = Usuario.objects.exclude(id__in=usuarios_ids)
        form = promoverAdm() #se tiver erro as informações do formulário voltam 
    return render(request, 'partials/usuario/formAdmMaster.html', {'form': form})

class RedirectAuthenticatedLoginView(BaseLoginView):
    """
    vai redirecionar os usuarios autenticados de volta para pagina anterior 
    (se caso tentarem acessar a pagina de login), a view vai herdar de loginview
    """
    # configura para redirecionar usuários autenticados automaticamente
    redirect_authenticated_user = True

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        """
        sobrescreve o método dispatch para verificar se o usuário está autenticado.
        se estiver, redireciona o usuário para a URL de onde ele veio.
        """
        # verifica se o usuário já está autenticado
        if request.user.is_authenticated:
            # pega URL da qual o usuário veio (HTTP_REFERER) ou redireciona para a URL padrão de login
            redirect_to = request.META.get('HTTP_REFERER', resolve_url(settings.LOGIN_REDIRECT_URL))
            # redireciona para a URL obtida
            return HttpResponseRedirect(redirect_to)
        # Caso o usuário não esteja autenticado, chama o método dispatch da classe base
        return super().dispatch(request, *args, **kwargs)
    
# def hadler404(request, exception):
#     return render(request, 'partials/404.html', status=404)