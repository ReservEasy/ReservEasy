from django.db import models
from django.db.models import Q
from recursos.models import Espaco, Equipamento
from usuario.models import Usuario

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reservas")
    dataHorarioSolicitacao = models.DateTimeField(auto_now_add=True)
    dataHorarioInicial = models.DateTimeField()
    dataHorarioFinal = models.DateTimeField()
    justificativa = models.CharField(max_length=200, blank=False, null=False)
    andamento = models.CharField(max_length=10, blank=False, null=False, choices=[
        ('em_analise', 'Em Análise'),
        ('negada', 'Negada'),
        ('aprovada', 'Aprovada')], default='em_analise')
    espacos = models.ManyToManyField(Espaco, related_name='reservasespaco', through='ReservaEspaco', blank=True)
    equipamentos = models.ManyToManyField(Equipamento, related_name='reservasequipamento', through='ReservaEquipamento', blank=True)
    situacao = models.CharField(max_length=2, blank=True, null=True)

    @staticmethod # staticmethod = método que não altera nada na classe e não precisa acessar instâncias
    def verificar_disponibilidade(dataHorarioInicial, dataHorarioFinal):
        # __lte = anterior __gte = posterior
        conflitos = (
            Q(dataHorarioInicial__lte=dataHorarioFinal, dataHorarioFinal__gte=dataHorarioInicial) &
            (
                Q(dataHorarioInicial__gte=dataHorarioInicial, dataHorarioInicial__lte=dataHorarioFinal) |
                Q(dataHorarioFinal__gte=dataHorarioInicial, dataHorarioFinal__lte=dataHorarioFinal) |
                Q(dataHorarioInicial__lte=dataHorarioInicial, dataHorarioFinal__gte=dataHorarioInicial) |
                Q(dataHorarioInicial__lte=dataHorarioFinal, dataHorarioFinal__gte=dataHorarioFinal)
            )
        )
        reservas_conflitantes = Reserva.objects.filter(conflitos, andamento='aprovada')
        
        espacos_indisponiveis = Espaco.objects.filter(reservasespaco__in=reservas_conflitantes).distinct()
        equipamentos_indisponiveis = Equipamento.objects.filter(reservasequipamento__in=reservas_conflitantes).distinct()
        
        espacos_disponiveis = Espaco.objects.exclude(pk__in=espacos_indisponiveis)
        equipamentos_disponiveis = Equipamento.objects.exclude(pk__in=equipamentos_indisponiveis)
        
        return espacos_disponiveis, equipamentos_disponiveis

class ReservaEspaco(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='reserva_espaco')
    espaco = models.ForeignKey(Espaco, on_delete=models.CASCADE, related_name='reserva_espaco')

class ReservaEquipamento(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='reserva_equipamento')
    recurso = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='reserva_equipamento')
    dataHorarioRetirada = models.DateTimeField(blank=True, null=True)
    dataHorarioDevolucao = models.DateTimeField(blank=True, null=True)
