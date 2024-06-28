from typing import Any
from django.forms import ModelForm
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name', 
            'last_name',
            'email',
            'matricula',
            'telefone',
            'turma',
            'data_nascimento',
            'cargo',
            'password1',
            'password2'
        ]

# mascara do input do form0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['telefone'].widget.attrs.update({'class': 'mask-telefone'})
        self.fields['data_nascimento'].widget.attrs.update({'class': 'mask-date'})