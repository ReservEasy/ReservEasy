# from django.contrib.auth.models import Group

# def criar_reserva(request):
#     if request.method == 'POST':
#         dataHorarioInicial = request.POST.get('dataHorarioInicial')
#         dataHorarioFinal = request.POST.get('dataHorarioFinal')
#         data_horario_inicial_dt = parse_datetime(dataHorarioInicial)
#         data_horario_final_dt = parse_datetime(dataHorarioFinal)

#         # Convertendo para timezone-aware
#         data_horario_inicial_dt = timezone.make_aware(data_horario_inicial_dt)
#         data_horario_final_dt = timezone.make_aware(data_horario_final_dt)

#         # Verificação de datas
#         if data_horario_inicial_dt < timezone.now():
#             messages.error(request, 'A data e hora inicial não pode ser no passado.')
#             return render(request, 'partials/reserva/formReserva.html', {'form': ReservaForm()})

#         if data_horario_inicial_dt >= data_horario_final_dt:
#             messages.error(request, 'A data e hora final deve ser posterior à data e hora inicial.')
#             return render(request, 'partials/reserva/formReserva.html', {'form': ReservaForm()})

#         if 'buscar' in request.POST:
#             espacos_disponiveis, equipamentos_disponiveis = Reserva.verificar_disponibilidade(data_horario_inicial_dt, data_horario_final_dt)
#             return render(request, 'partials/reserva/formReserva.html', {
#                 'espacos_disponiveis': espacos_disponiveis,
#                 'equipamentos_disponiveis': equipamentos_disponiveis,
#                 'dataHorarioInicial': dataHorarioInicial,
#                 'dataHorarioFinal': dataHorarioFinal
#             })
#         elif 'enviar_solicitacao' in request.POST:
#             justificativa = request.POST.get('justificativa')
#             espacos_selecionados = request.POST.getlist('espacos')
#             equipamentos_selecionados = request.POST.getlist('equipamentos')

#             if not espacos_selecionados and not equipamentos_selecionados or not justificativa:
#                 messages.error(request, 'Lembre-se que você deve selecionar pelo menos um espaço ou equipamento e preencher a justificativa.')
#                 espacos_disponiveis, equipamentos_disponiveis = Reserva.verificar_disponibilidade(data_horario_inicial_dt, data_horario_final_dt)
#                 return render(request, 'partials/reserva/formReserva.html', {
#                     'espacos_disponiveis': espacos_disponiveis,
#                     'equipamentos_disponiveis': equipamentos_disponiveis,
#                     'dataHorarioInicial': dataHorarioInicial,
#                     'dataHorarioFinal': dataHorarioFinal
#                 })

#             usuario = Usuario.objects.get(pk=request.user.pk)
#             andamento = 'em_analise'
#             if usuario.groups.filter(name__in=['Administrador de Setor', 'Administrador Master']).exists():
#                 andamento = 'aprovado'

#             reserva = Reserva.objects.create(
#                 usuario=usuario,
#                 dataHorarioInicial=data_horario_inicial_dt,
#                 dataHorarioFinal=data_horario_final_dt,
#                 justificativa=justificativa,
#                 andamento=andamento
#             )
#             for espaco_id in espacos_selecionados:
#                 espaco = Espaco.objects.get(pk=espaco_id)
#                 ReservaEspaco.objects.create(reserva=reserva, espaco=espaco)
#             for equipamento_id in equipamentos_selecionados:
#                 equipamento = Equipamento.objects.get(pk=equipamento_id)
#                 ReservaEquipamento.objects.create(reserva=reserva, recurso=equipamento)
#             return redirect('solicitacao_enviada', reserva_id=reserva.id)
#     else:
#         form = ReservaForm()
#     return render(request, 'partials/reserva/formReserva.html', {'form': form})
