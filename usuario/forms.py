from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    tipo = forms.IntegerField(widget=forms.HiddenInput())
    
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

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'matricula',
            'telefone',
            'data_nascimento',
            'turma',
            'cargo',
        ]
        widgets = {
            'turma': forms.TextInput(attrs={'placeholder': 'Turma'}),
            'cargo': forms.TextInput(attrs={'placeholder': 'Cargo'}),
        }

    def __init__(self, *args, **kwargs):
        # Obtém o usuário a partir dos argumentos
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.tipo == 1:
                # Se o usuário é do tipo 1, remova o campo 'cargo'
                self.fields.pop('cargo', None)
            elif user.tipo == 2:
                # Se o usuário é do tipo 2, remova o campo 'turma'
                self.fields.pop('turma', None)