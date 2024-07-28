from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReservaForm
from .models import Reserva, ReservaEspaco, ReservaEquipamento
from recursos.models import Equipamento, Espaco
from usuario.models import Usuario

@login_required
def criar_reserva(request):
    if request.method == 'POST':
        dataHorarioInicial = request.POST.get('dataHorarioInicial')
        dataHorarioFinal = request.POST.get('dataHorarioFinal')
        data_horario_inicial_dt = parse_datetime(dataHorarioInicial)
        data_horario_final_dt = parse_datetime(dataHorarioFinal)

        # Convertendo para timezone-aware
        data_horario_inicial_dt = timezone.make_aware(data_horario_inicial_dt)
        data_horario_final_dt = timezone.make_aware(data_horario_final_dt)

        # Verificação de datas
        if data_horario_inicial_dt < timezone.now():
            messages.error(request, 'A data e hora inicial não pode ser no passado.')
            return render(request, 'partials/reserva/testandoReserva.html', {'form': ReservaForm()})

        if data_horario_inicial_dt >= data_horario_final_dt:
            messages.error(request, 'A data e hora final deve ser posterior à data e hora inicial.')
            return render(request, 'partials/reserva/testandoReserva.html', {'form': ReservaForm()})

        if 'buscar' in request.POST:
            espacos_disponiveis, equipamentos_disponiveis = Reserva.verificar_disponibilidade(data_horario_inicial_dt, data_horario_final_dt)
            return render(request, 'partials/reserva/testandoReserva.html', {
                'espacos_disponiveis': espacos_disponiveis,
                'equipamentos_disponiveis': equipamentos_disponiveis,
                'dataHorarioInicial': dataHorarioInicial,
                'dataHorarioFinal': dataHorarioFinal
            })
        elif 'enviar_solicitacao' in request.POST:
            justificativa = request.POST.get('justificativa')
            espacos_selecionados = request.POST.getlist('espacos')
            equipamentos_selecionados = request.POST.getlist('equipamentos')

            if not espacos_selecionados and not equipamentos_selecionados or not justificativa:
                messages.error(request, 'Lembre-se que você deve selecionar pelo menos um espaço ou equipamento e preencher a justificativa.')
                espacos_disponiveis, equipamentos_disponiveis = Reserva.verificar_disponibilidade(data_horario_inicial_dt, data_horario_final_dt)
                return render(request, 'partials/reserva/testandoReserva.html', {
                    'espacos_disponiveis': espacos_disponiveis,
                    'equipamentos_disponiveis': equipamentos_disponiveis,
                    'dataHorarioInicial': dataHorarioInicial,
                    'dataHorarioFinal': dataHorarioFinal
                })

            reserva = Reserva.objects.create(
                usuario=Usuario.objects.get(pk=request.user.pk),
                dataHorarioInicial=data_horario_inicial_dt,
                dataHorarioFinal=data_horario_final_dt,
                justificativa=justificativa
            )
            for espaco_id in espacos_selecionados:
                espaco = Espaco.objects.get(pk=espaco_id)
                ReservaEspaco.objects.create(reserva=reserva, espaco=espaco)
            for equipamento_id in equipamentos_selecionados:
                equipamento = Equipamento.objects.get(pk=equipamento_id)
                ReservaEquipamento.objects.create(reserva=reserva, recurso=equipamento)
            return redirect('listar_reservas')
    else:
        form = ReservaForm()
    return render(request, 'partials/reserva/testandoReserva.html', {'form': form})

@login_required
def listar_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'partials/reserva/lista_reserva.html', {'reservas': reservas})
