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
            'password'
        ]
        #falta telefone, add depois para arrumar erro do template