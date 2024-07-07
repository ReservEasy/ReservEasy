from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.template import loader
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from .forms import UsuarioForm


# def index(request):
#     return HttpResponse("Hello, world. You're at the rua index.")
# converte a senha em um hash

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


#metodo que lista todos os registros

    