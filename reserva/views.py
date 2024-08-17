from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from .forms import ReservaForm
from django.contrib.auth.models import Group
from .models import Reserva, ReservaEspaco, ReservaEquipamento
from recursos.models import Equipamento, Espaco
from usuario.models import Usuario
from setor.models import Setor
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta

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
            return render(request, 'partials/reserva/formReserva.html', {'form': ReservaForm()})

        if data_horario_inicial_dt >= data_horario_final_dt:
            messages.error(request, 'A data e hora final deve ser posterior à data e hora inicial.')
            return render(request, 'partials/reserva/formReserva.html', {'form': ReservaForm()})

        if 'buscar' in request.POST:
            espacos_disponiveis, equipamentos_disponiveis = Reserva.verificar_disponibilidade(data_horario_inicial_dt, data_horario_final_dt)
            return render(request, 'partials/reserva/formReserva.html', {
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
                return render(request, 'partials/reserva/formReserva.html', {
                    'espacos_disponiveis': espacos_disponiveis,
                    'equipamentos_disponiveis': equipamentos_disponiveis,
                    'dataHorarioInicial': dataHorarioInicial,
                    'dataHorarioFinal': dataHorarioFinal
                })
            usuario = Usuario.objects.get(pk=request.user.pk)
            andamento = 'em_analise'
            if usuario.groups.filter(name__in=['Administrador de Setor', 'Administrador Master']).exists():
                andamento = 'aprovada'

            reserva = Reserva.objects.create(
                usuario=Usuario.objects.get(pk=request.user.pk),
                dataHorarioInicial=data_horario_inicial_dt,
                dataHorarioFinal=data_horario_final_dt,
                justificativa=justificativa,
                andamento=andamento
            )
            for espaco_id in espacos_selecionados:
                espaco = Espaco.objects.get(pk=espaco_id)
                ReservaEspaco.objects.create(reserva=reserva, espaco=espaco)
            for equipamento_id in equipamentos_selecionados:
                equipamento = Equipamento.objects.get(pk=equipamento_id)
                ReservaEquipamento.objects.create(reserva=reserva, recurso=equipamento)
            return redirect('solicitacao_enviada', reserva_id=reserva.id)
    else:
        form = ReservaForm()
    return render(request, 'partials/reserva/formReserva.html', {'form': form})

@login_required
def solicitacaoEnviada(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    if request.user.groups.filter(name="Administrador Master").exists():
        tipo_adm = "Adm Master"
    elif request.user.groups.filter(name="Administrador de Setor").exists():
        tipo_adm = "Adm Setor"
    else:
        tipo_adm = "Solicitante"
    return render(request, 'partials/reserva/formReserva_done.html', {
        'dataHorarioInicial': reserva.dataHorarioInicial,
        'dataHorarioFinal': reserva.dataHorarioFinal,
        'codigo_solicitacao': reserva_id,
        'tipo_adm': tipo_adm,
    })

# @login_required
# def listar_reservas(request):
#     reservas = Reserva.objects.all()
#     return render(request, 'partials/reserva/lista_reserva.html', {'reservas': reservas})

@login_required
def listar_reservas_usuario(request):
    user = request.user.id
    usuario = Usuario.objects.get(pk=user)
    reservas = usuario.reservas.all().order_by('-id')  # Corrigido para usar o related_name correto
    quant_reservas = len(reservas)
    for reserva in reservas:
        print(reserva.id)
    paginator = Paginator(reservas, 6)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, 'partials/reserva/user/listarSolicitacoesUser.html',{
        'reservas': page_obj,
        'page_obj': page_obj,
        'quant_reservas': quant_reservas
    })

@login_required
def detalharReserva(request, id_reserva):
    reserva = Reserva.objects.get(pk=id_reserva)
    id_user = reserva.usuario
    usuario = Usuario.objects.get(pk=id_user)
    user = request.user.id
    usuarioatual = Usuario.objects.get(pk=user)
    return render(request, "partials/reserva/acoes/detalharSolicitacao.html",{
        'reserva': reserva,
        'usuario': usuario,
        'usuarioatual': usuarioatual
    })

@login_required
def deletarReserva(request, id_reserva):
    user = request.user.id
    usuario = Usuario.objects.get(pk=user)
    reservaa = Reserva.objects.get(pk=id_reserva)
    reservas = usuario.reservas.all() 
    liberado = 'nao'
    if reservas:
        for reserva in reservas:
            if reserva.id == reservaa.id:
                liberado = 'sim'
    if liberado == 'nao':
        return HttpResponseForbidden("Você não tem permissão para deletar esta reserva.")
    else:
        reservaa.delete()
        return redirect('/reserva/listar')

def usuario_ou_admin_master(u):
    return u.groups.filter(name__in=['Administrador de Setor', 'Administrador Master']).exists()

@user_passes_test(usuario_ou_admin_master)
def historicoSolicitacao(request):
    search_query = request.GET.get('searchbar', '') 
    if search_query:
        reservas_list = Reserva.objects.filter(
            Q(usuario__username__icontains=search_query)
        ).order_by('-id')
    else:
        reservas_list = Reserva.objects.all().order_by('-id')

    total_reservas = reservas_list.count()  # Total de reservas

    # Paginação
    paginator = Paginator(reservas_list, 8)  # Mostra 8 reservas por página
    page_number = request.GET.get('page')
    reservas = paginator.get_page(page_number)

    return render(request, "partials/reserva/historico/historicoSolicitacoes.html", {
        'reservas': reservas,
        'total_reservas': total_reservas,
        'search_query': search_query,
        'page_obj': reservas
    })

@user_passes_test(lambda u: u.groups.filter(name__in=['Administrador de Setor', 'Administrador Master']).exists())
def acessarDashboard(request):

    data_posterior = (timezone.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    hoje = date.today()
    # contando as reservas em análise
    solicitacoes_analisar = Reserva.objects.filter(andamento='em_analise').count()

    reservas_hoje = Reserva.objects.filter(
        dataHorarioInicial__date=hoje,
        andamento='aprovada'
    ).count()

    # detalhes das reservas para hoje
    reservas_hoje_detalhes = Reserva.objects.filter(
        dataHorarioInicial__date=hoje,
        andamento='aprovada'
    )
    
    contar = 5 - reservas_hoje
    reservas_proximas = Reserva.objects.filter(dataHorarioInicial__gte=data_posterior, andamento='aprovada').order_by('dataHorarioInicial')[:contar]

    # determina o tipo de administrador
    if request.user.groups.filter(name='Administrador Master').exists():
        tipo_adm = 'Adm Master'
    elif request.user.groups.filter(name='Administrador de Setor').exists():
        tipo_adm = 'Adm Setor'
    else:
        tipo_adm = 'Solicitante'

    # total de usuários registrados
    usuarios_list = Usuario.objects.all()
    total_usuarios = usuarios_list.count()

    # total de setores registrados
    setores_list = Setor.objects.all()
    total_setores = setores_list.count()  

    # total de solicitacoes registrados
    reservas_list = Reserva.objects.all()
    total_solicitacoes = reservas_list.count()  # Total de reservas

    context = {
        'tipo_adm': tipo_adm,
        'total_usuarios': total_usuarios,
        'total_solicitacoes': total_solicitacoes,
        'total_setores': total_setores,
        'solicitacoes_analisar': solicitacoes_analisar,
        'reservas_hoje': reservas_hoje,
        'reservas_hoje_detalhes': reservas_hoje_detalhes,
        'reservas_proximas': reservas_proximas,
    }

    return render(request, 'partials/dashboard.html', context)

@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def solicitacoes(request):
    search_query = request.GET.get('searchbar', '')
    if search_query:
        usuarios_list = Usuario.objects.filter(
            first_name__icontains=search_query
        ) | Usuario.objects.filter(
            last_name__icontains=search_query
        )
    else:
        usuarios_list = Usuario.objects.all()

    solicitacoes_em_analise = Reserva.objects.filter(andamento='em_analise').order_by('-id')
    paginator = Paginator(solicitacoes_em_analise, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "partials/reserva/acoes/listarSolicitacoes.html", {
        'reservas': page_obj.object_list,
        'page_obj': page_obj,
        'usuarios': usuarios_list,  
        'search_query': search_query 
    })

@user_passes_test(lambda u: u.groups.filter(name='Administrador de Setor').exists())
def atualizar_status_reserva(request, reserva_id, status):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    # Verificação de conflito
    conflito = False
    reservas_conflitantes = Reserva.objects.filter(
        Q(espacos__in=reserva.espacos.all()) | Q(equipamentos__in=reserva.equipamentos.all()),
        andamento='aprovada'
    ).filter(
        Q(dataHorarioInicial__lte=reserva.dataHorarioFinal, dataHorarioFinal__gte=reserva.dataHorarioInicial) & 
        (
            Q(dataHorarioInicial__gte=reserva.dataHorarioInicial, dataHorarioInicial__lte=reserva.dataHorarioFinal) |
            Q(dataHorarioFinal__gte=reserva.dataHorarioInicial, dataHorarioFinal__lte=reserva.dataHorarioFinal) |
            Q(dataHorarioInicial__lte=reserva.dataHorarioInicial, dataHorarioFinal__gte=reserva.dataHorarioInicial) |
            Q(dataHorarioInicial__lte=reserva.dataHorarioFinal, dataHorarioFinal__gte=reserva.dataHorarioFinal)
        )
    ).distinct()

    if reservas_conflitantes.exists():
        conflito = True
        status = 'negada'

    # Atualiza o status da reserva
    if status in ['aprovada', 'negada']:
        reserva.andamento = status
        reserva.save()

    return redirect('/reserva/solicitacoes/analise/')