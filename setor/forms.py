from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Setor
from usuario.models import Usuario

class SetorForm(ModelForm):
    class Meta:
        model = Setor
        fields = [
            'nome'
        ]
        
class AlocarAdm(forms.Form):
    usuarios = forms.ModelMultipleChoiceField( #permite selecionar vários campos
        queryset=Usuario.objects.filter(setor__isnull=True, tipo=2),  # Filtra usuários sem setor atribuído
        widget=forms.CheckboxSelectMultiple,  # Exibe com caixas de seleção
        required=True  #obriga a selção de pelo menos uma caixa
    )