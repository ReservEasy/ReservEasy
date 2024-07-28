from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['telefone'].widget.attrs.update({'class': 'mask-telefone'})
        self.fields['data_nascimento'].widget.attrs.update({'class': 'mask-date'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Já existe um usuário com esse email.")
        return email
