from django.shortcuts import render
from django.db import Error
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Recurso
from .forms import RecursoForm
from django.contrib.auth.models import Group
# from braces.views import GroupRequiredMixin


def index(request):
    return HttpResponse("Hello, world. You're at the recurso index.")

@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def criar(request):
    if request.method == 'POST':
        form = RecursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/recursos/?msg=Salvo')
    else:
        form = RecursoForm()
    return render(request, 'partials/recurso/formRecurso.html', {'form':form})

#metodo que lista todos os registros
@login_required
def listarRecursos(request):
    user = request.user
    administrador_setor = Group.objects.get(name='Administrador de Setor')
    is_admin_setor = administrador_setor in user.groups.all()

    recursos = Recurso.objects.all()
    return render(request, "partials/recurso/listarRecursos.html", {'recursos': recursos, 'is_admin_setor': is_admin_setor})

@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists()) 
def editar(request, id_recurso):
    recurso = Recurso.objects.get(pk=id_recurso)
    if request.method == 'POST':
        form = RecursoForm(request.POST, request.FILES, instance= recurso)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/recursos/?msg=Salvo')
    else:
        form = RecursoForm(instance= recurso)
    return render(request, 'partials/recurso/editarRecursos.html', {'form':form, 'id_recurso': id_recurso})


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists()) 
def deletar(request, id_recurso):
    Recurso.objects.get(pk=id_recurso).delete()

    return HttpResponseRedirect("/recursos/?msg=Exclui")


@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists()) 
def confirmarDelete(request, id_recurso):
    recurso = Recurso.objects.get(pk=id_recurso)

    return render (request, 'partials/recurso/confirmaExcluir.html', {'recurso':recurso})


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

    