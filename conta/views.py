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
    return render(request, 'registration/register.html', {'form':form})

#metodo que lista todos os registros

    