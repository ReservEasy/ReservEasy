from django import forms
from django.forms import ModelForm
from .models import Equipamento, Espaco

class EquipamentoForm(ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'quantTotal', 'descricao', 'imagem'  ]
        labels = {
            'nome': 'Nome do Equipamento',
            'quantTotal': 'Quantidade Total',
            'descricao': 'Descrição',
            'imagem': 'Imagem',
        }
class EspacoForm(ModelForm):
    class Meta:
        model = Espaco
        fields = ['nome', 'localizacao', 'descricao', 'imagem']
        labels = {
            'nome': 'Nome do Espaço',
            'imagem': 'Imagem',
            'descricao': 'Descrição',
            'localizacao': 'Localização',
        }
        
# class RecursoForm(ModelForm):
#     class Meta:
#         model = Recurso
#         fields = ['nome','imagem', 'descricao', 'tipo', 'quantidade']

