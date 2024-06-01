from django import forms
from django.forms import ModelForm
from .models import Recurso

class RecursoForm(ModelForm):
    class Meta:
        model = Recurso
        fields = ['nome','imagem', 'descricao', 'tipo']

