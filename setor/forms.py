from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Setor

class SetorForm(ModelForm):
    class Meta:
        model = Setor
        fields = [
            'nome'
        ]
