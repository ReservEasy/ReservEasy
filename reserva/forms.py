from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Reserva
from recursos.models import Espaco, Equipamento

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['dataHorarioInicial', 'dataHorarioFinal', 'espacos', 'equipamentos', 'justificativa']

    dataHorarioInicial = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data e Hora Inicial",
    )
    dataHorarioFinal = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data e Hora Final",
    )

    espacos = forms.ModelMultipleChoiceField(
        queryset=Espaco.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Espaços",
        required=False,  # Espaços agora é opcional
    )
    equipamentos = forms.ModelMultipleChoiceField(
        queryset=Equipamento.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Equipamentos",
        required=False,  # Equipamentos agora é opcional
    )

    def clean(self):
        cleaned_data = super().clean()
        espacos = cleaned_data.get('espacos')
        equipamentos = cleaned_data.get('equipamentos')

        # if not espacos and not equipamentos:
        #     raise forms.ValidationError("Você deve selecionar pelo menos um espaço ou um equipamento.")
        # return cleaned_data
    
    # def clean_dataHorarioInicial(self):
    #     data = self.cleaned_data.get('dataHorarioInicial')
    #     now = timezone.localtime(timezone.now())
    #     margem = timedelta(minutes=1)  # Define uma margem de 1 minuto
    #     if data and data < (now - margem):
    #         raise forms.ValidationError("A data e hora inicial não pode ser no passado.")
    #     return data

    # def clean_dataHorarioFinal(self):
    #     data_inicial = self.cleaned_data.get('dataHorarioInicial')
    #     data_final = self.cleaned_data.get('dataHorarioFinal')
    #     if data_inicial and data_final and data_final <= data_inicial:
    #         raise forms.ValidationError("A data e hora final deve ser posterior à data e hora inicial.")
    #     return data_final
