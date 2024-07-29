from django.shortcuts import render, redirect, get_object_or_404
from django.db import Error
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Setor
from usuario.models import Usuario
from recursos.models import Espaco, Equipamento
from .forms import SetorForm, AlocarAdm
from django.contrib.auth.models import Group
import os
from django.core.paginator import Paginator
from django.urls import reverse
from urllib.parse import urlencode

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
    search_query = request.GET.get('searchbar', '') # pega o parâmetro de pesquisa
    setores_list = Setor.objects.all()
    if search_query:
        setores_list = setores_list.filter(
            nome__icontains=search_query
        )
    # paginação
    paginator = Paginator(setores_list, 10)  # mostra apenas 10 setores por página
    page_number = request.GET.get('page')
    setores = paginator.get_page(page_number)
    
    total_setores = setores_list.count()  # total de setores registrados
    
    return render(request, "partials/setor/listarSetores.html", {
        'setores': setores,
        'total_setores': total_setores,
        'search_query': search_query
    })

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def detalharSetor(request, id_setor):
    setor = Setor.objects.get(pk=id_setor)

    usuarios = setor.usuarios.all() # pega todos os usuarios que fazem parte do setor selecionado
    total_usuarios = len(usuarios)  # total de usuarios registrados no setor
    equipamentos = setor.equipamentos.all()  # Todos os equipamentos associados ao setor
    espacos = setor.espacos.all()  # Todos os espaços associados ao setor
    recursos = list(equipamentos) + list(espacos) #junta os espacos e equipamentos dentro de recursos
    total_recursos = len(recursos)  # total de recursos registrados no setor
    return render(request, "partials/setor/detalharSetor.html",{
        'setor': setor,
        'usuarios': usuarios,
        'total_usuarios': total_usuarios,
        'recursos': recursos,
        'total_recursos': total_recursos
    })

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def alocarAdm(request, id_setor):
    setor = Setor.objects.get(id=id_setor)

    if request.method == 'POST': #se receber um formulario
        form = AlocarAdm(request.POST) #armazena o que obteve pelo form
        if form.is_valid():
            usuarios = form.cleaned_data['usuarios'] #pega a lista dos usuarios selecionados
            for usuario in usuarios: #for para definir o atributo setor dos usuarios selecionados com o id do setor atual
                group, created = Group.objects.get_or_create(name='Administrador de Setor')  # Obtém ou cria o grupo
                usuario.groups.set([group])  # Define o grupo do usuário como o grupo 'Administrador de Setor' (remove qualquer outro que tinha antes)
                usuario.setor = setor
                usuario.save()
            return redirect(reverse('detalharSetor', args=[id_setor])) # retorna para a pagina de detalhar o setor
    else:
        form = AlocarAdm() #se tiver erro as informações do formulário voltam 

    return render(request, 'partials/setor/formAdmSetor.html', {'form': form, 'setor': setor})

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def removerAdm(request, id_adm):
    usuario = Usuario.objects.get(id=id_adm)

    id_setor = usuario.setor.id if usuario.setor else None   # busca que o setor está associado ao usuário

    group, created = Group.objects.get_or_create(name='Solicitante')  # Obtém ou cria o grupo
    usuario.groups.set([group])  # Define o grupo do usuário como o grupo 'Solicitante' (remove qualquer outro que tinha antes)
    usuario.setor = None
    usuario.save()

    url = reverse('detalharSetor', args=[id_setor]) 
    query_string = urlencode({'msg': 'salvo'})
    redirect_url = f'{url}?{query_string}'
    return redirect(redirect_url) #retorna a pagina anterior com o id setor


@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def transferirAdm(request, id_adm):
    usuario = Usuario.objects.get(id=id_adm) 
    idsetor= usuario.setor_id
    if request.method == 'POST':
        novo_setor_id = request.POST.get('setor')
        novo_setor = get_object_or_404(Setor, id=novo_setor_id)  # Obtém a instância do setor com base no ID
        usuario.setor = novo_setor  
        usuario.save()
        return HttpResponseRedirect('/setor/?msg=Salvo')
    setores = Setor.objects.all()
    return render(request, 'partials/setor/formTransferirAdm.html', {'usuario': usuario, 'setores': setores, 'idsetor': idsetor})

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
    return render(request, 'partials/setor/editarSetor.html', {'form': form, 'id_setor': id_setor, 'setor': setor})

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm master
def deletar(request, id_setor):
    Setor.objects.get(pk=id_setor).delete()

    return HttpResponseRedirect("/setor/?msg=Exclui")

@user_passes_test(lambda u: u.groups.filter(name='Administrador Master').exists()) #só acessa se for adm masterb
def confirmarDelete(request, id_setor):
    setor = Setor.objects.get(pk=id_setor)

    return render (request, 'partials/setor/confirmaExcluirSetor.html', {'setor':setor})
