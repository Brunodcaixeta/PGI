import json
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Eixo, Area, AcaoInstitucional, AtualizacaoAcao, Etapa, UserAssessor


# ────────────────────────────────────────────────────────
# Mapeamento de ícones Material Symbols para cada eixo.
# Cada eixo ganha um ícone representativo do seu tema.
# ────────────────────────────────────────────────────────
EIXO_ICONS = {
    'Direitos': 'gavel',
    'Reconhecimento da Atuação': 'emoji_events',
    'Fortalecimento Institucional': 'shield',
    'Valorização da Carreira': 'trending_up',
    'Modernização das Instalações': 'domain',
    'Aperfeiçoamento Institucional': 'tune',
    'Gestão do Conhecimento': 'school',
    'Apoio Técnico e Operacional': 'build',
    'Automação Inteligente': 'smart_toy',
    'Integração Sistêmica': 'hub',
    'Atualização Contínua': 'update',
    'Investigação': 'search',
    'Segurança': 'security',
    'Articulação Externa Estratégica': 'handshake',
    'Diálogo Interno Fortalecido': 'forum',
    'Defesa Permanente': 'verified_user',
    'Parcerias Institucionais': 'groups',
    'Pesquisa e Produção Acadêmica': 'science',
    'Gestão do Conhecimento e Biblioteca': 'menu_book',
    'Saúde, Qualidade de Vida e Ambiente Institucional': 'favorite',
    'Gestão de Pessoas e Carreiras': 'people',
    'Equidade, Inclusão e Diversidade': 'diversity_3',
}

# Cores de destaque que ciclam entre os cards para variedade visual
ACCENT_COLORS = [
    '#0ea5e9',  # azul
    '#22c55e',  # verde
    '#a855f7',  # roxo
    '#eab308',  # amarelo
    '#ec4899',  # rosa
    '#f97316',  # laranja
    '#22d3ee',  # ciano
    '#ef4444',  # vermelho
]


def home(request):
    """
    View da tela inicial — Visão Geral do Plano.

    Consulta o banco de dados para montar:
    - Lista de Eixos com evolução média e contagem de ações
    - Lista de Áreas com evolução média e contagem de ações
    - Progresso Global (média geral de todas as ações)
    """

    # ────────────────────────────────────────────────────────
    # ETAPA 1: Descobrir a evolução atual de cada Ação
    #
    # Cada ação pode ter N atualizações (tabela AtualizacaoAcao).
    # A evolução "atual" é o valor_evolucao da atualização
    # mais recente (ordenada por data).
    #
    # prefetch_related('atualizacoes') carrega TODAS as
    # atualizações de TODAS as ações em apenas 2 queries SQL
    # (uma para ações, uma para atualizações), evitando o
    # problema N+1.
    # ────────────────────────────────────────────────────────

    acoes = AcaoInstitucional.objects.prefetch_related('atualizacoes').all()

    # Dicionário: { acao_id: evolução_atual (float) }
    evolucao_por_acao = {}

    for acao in acoes:
        # Ordena as atualizações pela data (mais recente primeiro)
        atualizacoes = sorted(
            acao.atualizacoes.all(),
            key=lambda a: a.data_atualizacao,
            reverse=True,
        )
        # Pega o valor_evolucao da atualização mais recente
        if atualizacoes and atualizacoes[0].valor_evolucao is not None:
            evolucao_por_acao[acao.id] = float(atualizacoes[0].valor_evolucao)
        else:
            evolucao_por_acao[acao.id] = 0.0

    # ────────────────────────────────────────────────────────
    # ETAPA 2: Calcular evolução média por EIXO
    #
    # Para cada eixo, pega todas as suas ações, busca a
    # evolução de cada uma no dicionário, e calcula a média.
    # Também atribui um ícone e uma cor de destaque.
    # ────────────────────────────────────────────────────────

    eixos = Eixo.objects.prefetch_related('acoes').all()
    eixos_data = []
    todas_evolucoes = []  # acumula para calcular o progresso global

    for i, eixo in enumerate(eixos):
        acoes_do_eixo = list(eixo.acoes.all())
        evolucoes = [evolucao_por_acao.get(a.id, 0) for a in acoes_do_eixo]
        media = sum(evolucoes) / len(evolucoes) if evolucoes else 0
        todas_evolucoes.extend(evolucoes)

        eixos_data.append({
            'id': eixo.id,
            'numero': f'{i + 1:02d}',  # "01", "02", etc.
            'nome': eixo.eixo,
            'num_acoes': len(acoes_do_eixo),
            'evolucao': round(media * 100, 1),  # 0-1 → 0-100%
            'icon': EIXO_ICONS.get(eixo.eixo, 'category'),
            'cor': ACCENT_COLORS[i % len(ACCENT_COLORS)],
        })

    # ────────────────────────────────────────────────────────
    # ETAPA 3: Calcular evolução média por ÁREA
    # ────────────────────────────────────────────────────────

    areas = Area.objects.prefetch_related('acoes').all()
    areas_data = []

    for i, area in enumerate(areas):
        acoes_da_area = list(area.acoes.all())
        evolucoes = [evolucao_por_acao.get(a.id, 0) for a in acoes_da_area]
        media = sum(evolucoes) / len(evolucoes) if evolucoes else 0

        areas_data.append({
            'id': area.id,
            'numero': f'{i + 1:02d}',
            'sigla': area.sigla or '',
            'nome': area.nome_area,
            'num_acoes': len(acoes_da_area),
            'evolucao': round(media * 100, 1),  # 0-1 → 0-100%
            'cor': ACCENT_COLORS[i % len(ACCENT_COLORS)],
            'atuacao_fim': area.atuacao,
        })

    # ────────────────────────────────────────────────────────
    # ETAPA 4: Progresso Global
    # Média de todas as evoluções de todas as ações.
    # ────────────────────────────────────────────────────────

    progresso_global = round(
        (sum(todas_evolucoes) / len(todas_evolucoes)) * 100, 1
    ) if todas_evolucoes else 0

    # ────────────────────────────────────────────────────────
    # ETAPA 5: Montar o contexto e renderizar
    #
    # Tudo que está no dicionário 'context' fica disponível
    # dentro do template HTML via {{ nome_da_variavel }}.
    # ────────────────────────────────────────────────────────

    context = {
        'eixos': eixos_data,
        'areas': areas_data,
        'progresso_global': progresso_global,
        'total_eixos': len(eixos_data),
        'total_areas': len(areas_data),
        'total_acoes': len(acoes),
    }

    return render(request, 'pgi/home.html', context)


def eixo_detail(request, eixo_id):
    """
    View de detalhes de um Eixo — lista suas Ações Institucionais.

    Cada ação exibe: descrição, código, área, responsável e evolução (%).
    As etapas de cada ação são carregadas para serem exibidas
    sob demanda (expand/collapse no front-end).
    """

    # ────────────────────────────────────────────────────────
    # 1. Buscar o eixo pelo ID (retorna 404 se não existir)
    # ────────────────────────────────────────────────────────
    eixo = get_object_or_404(Eixo, pk=eixo_id)

    # ────────────────────────────────────────────────────────
    # 2. Buscar todas as ações deste eixo, com dados relacionados
    #
    # select_related = JOIN (para ForeignKey, traz tudo em 1 query)
    # prefetch_related = query separada (para relações reversas)
    # ────────────────────────────────────────────────────────
    acoes = (
        AcaoInstitucional.objects
        .filter(eixo=eixo)
        .select_related('area', 'responsavel', 'responsavel_suplan')
        .prefetch_related('atualizacoes', 'etapas__responsavel')
        .order_by('ordem', 'codigo')
    )

    # ────────────────────────────────────────────────────────
    # 3. Para cada ação, calcular a evolução atual e
    #    preparar a lista de etapas ordenadas
    # ────────────────────────────────────────────────────────
    acoes_data = []
    todas_evolucoes = []

    for acao in acoes:
        # Evolução: última atualização
        atualizacoes = sorted(
            acao.atualizacoes.all(),
            key=lambda a: a.data_atualizacao,
            reverse=True,
        )
        if atualizacoes and atualizacoes[0].valor_evolucao is not None:
            evolucao = float(atualizacoes[0].valor_evolucao) * 100
        else:
            evolucao = 0.0
        todas_evolucoes.append(evolucao)

        # Etapas ordenadas
        etapas = list(
            acao.etapas
            .filter(bl_deletado=False)
            .order_by('ordem', 'id')
        )
        total_etapas = len(etapas)
        etapas_concluidas = sum(1 for e in etapas if e.concluido)

        # Responsável formatado
        resp_nome = ''
        if acao.responsavel:
            resp_nome = str(acao.responsavel)

        # Permissão de edição: responsável, admin, gestor_chefe, superuser ou assessor
        pode_editar = False
        if request.user.is_authenticated:
            u = request.user
            eh_assessor = (
                acao.responsavel_id
                and UserAssessor.objects.filter(
                    titular_id=acao.responsavel_id,
                    assessor_id=u.id,
                ).exists()
            )
            pode_editar = (
                u.is_superuser
                or getattr(u, 'admin', False)
                or getattr(u, 'gestor_chefe', False)
                or (acao.responsavel_id and acao.responsavel_id == u.id)
                or eh_assessor
            )

        acoes_data.append({
            'id': acao.id,
            'codigo': acao.codigo or '—',
            'acao': acao.acao,
            'area_sigla': acao.area.sigla or '',
            'area_nome': acao.area.nome_area,
            'responsavel': resp_nome,
            'evolucao': round(evolucao, 1),
            'etapas': etapas,
            'total_etapas': total_etapas,
            'etapas_concluidas': etapas_concluidas,
            'pode_editar': pode_editar,
        })

    # Evolução média do eixo
    evolucao_eixo = round(
        sum(todas_evolucoes) / len(todas_evolucoes), 1
    ) if todas_evolucoes else 0

    # Ícone e cor do eixo (reusar mapeamentos da home)
    eixo_idx = list(Eixo.objects.values_list('id', flat=True)).index(eixo_id)
    icon = EIXO_ICONS.get(eixo.eixo, 'category')
    cor = ACCENT_COLORS[eixo_idx % len(ACCENT_COLORS)]

    context = {
        'eixo': eixo,
        'eixo_icon': icon,
        'eixo_cor': cor,
        'eixo_evolucao': evolucao_eixo,
        'acoes': acoes_data,
        'total_acoes': len(acoes_data),
    }

    return render(request, 'pgi/eixo_detail.html', context)


@login_required
@require_POST
def atualizar_evolucao(request, acao_id):
    """
    Endpoint AJAX para atualizar o percentual de evolução de uma Ação.

    - Aceita apenas POST
    - Exige usuário autenticado
    - Valida permissão: responsável, admin, gestor_chefe ou superuser
    - Cria novo registro em AtualizacaoAcao preservando valor anterior
    - Retorna JSON para atualização dinâmica do front-end
    """
    acao = get_object_or_404(AcaoInstitucional, pk=acao_id)

    # ── Verificar permissão ──
    u = request.user
    pode_editar = (
        u.is_superuser
        or getattr(u, 'admin', False)
        or getattr(u, 'gestor_chefe', False)
        or (acao.responsavel_id and acao.responsavel_id == u.id)
    )
    if not pode_editar:
        return JsonResponse(
            {'success': False, 'error': 'Você não tem permissão para atualizar esta ação.'},
            status=403,
        )

    # ── Extrair e validar o novo percentual ──
    try:
        body = json.loads(request.body)
        novo_percentual = Decimal(str(body.get('novo_percentual', '')))
    except (json.JSONDecodeError, InvalidOperation, TypeError):
        return JsonResponse(
            {'success': False, 'error': 'Valor inválido. Envie um número entre 0 e 100.'},
            status=400,
        )

    if novo_percentual < 0 or novo_percentual > 100:
        return JsonResponse(
            {'success': False, 'error': 'O valor deve estar entre 0 e 100.'},
            status=400,
        )

    # ── Buscar valor anterior (última atualização) ──
    ultima = (
        AtualizacaoAcao.objects
        .filter(acao=acao)
        .order_by('-data_atualizacao')
        .first()
    )
    valor_anterior = ultima.valor_evolucao if ultima else Decimal('0.00')

    # ── Criar novo registro de atualização ──
    valor_evolucao = novo_percentual / Decimal('100')  # 0–100 → 0.00–1.00

    AtualizacaoAcao.objects.create(
        acao=acao,
        valor_anterior=valor_anterior,
        valor_evolucao=valor_evolucao,
        atualizacao_percentual=True,
        responsavel_registro=u,
    )

    return JsonResponse({
        'success': True,
        'novo_valor': float(novo_percentual),
        'valor_anterior': float(valor_anterior) * 100,
    })


@login_required
@require_POST
def criar_etapa(request, acao_id):
    """
    Endpoint AJAX para cadastrar uma nova Etapa em uma Ação Institucional.

    - Aceita apenas POST
    - Exige usuário autenticado
    - Valida permissão: responsável, assessor, admin, gestor_chefe ou superuser
    - Calcula automaticamente: ordem, etapa_referencia, responsável
    - Retorna JSON com dados da etapa criada
    """
    acao = get_object_or_404(AcaoInstitucional, pk=acao_id)

    # ── Verificar permissão ──
    u = request.user
    eh_assessor = (
        acao.responsavel_id
        and UserAssessor.objects.filter(
            titular_id=acao.responsavel_id,
            assessor_id=u.id,
        ).exists()
    )
    pode_editar = (
        u.is_superuser
        or getattr(u, 'admin', False)
        or getattr(u, 'gestor_chefe', False)
        or (acao.responsavel_id and acao.responsavel_id == u.id)
        or eh_assessor
    )
    if not pode_editar:
        return JsonResponse(
            {'success': False, 'error': 'Você não tem permissão para cadastrar etapas nesta ação.'},
            status=403,
        )

    # ── Extrair e validar a descrição ──
    try:
        body = json.loads(request.body)
        descricao = body.get('descricao', '').strip()
    except (json.JSONDecodeError, TypeError):
        return JsonResponse(
            {'success': False, 'error': 'Dados inválidos.'},
            status=400,
        )

    if not descricao:
        return JsonResponse(
            {'success': False, 'error': 'A descrição da etapa é obrigatória.'},
            status=400,
        )

    # ── Calcular próxima ordem e etapa_referencia ──
    ultima_ordem = (
        Etapa.objects
        .filter(acao=acao, bl_deletado=False)
        .aggregate(max_ordem=Max('ordem'))
    )['max_ordem'] or 0
    nova_ordem = ultima_ordem + 1

    codigo_acao = acao.codigo or f'A{acao.id}'
    etapa_ref = f'{codigo_acao}-{nova_ordem}'

    # ── Criar a etapa ──
    etapa = Etapa.objects.create(
        acao=acao,
        etapa=descricao,
        etapa_referencia=etapa_ref,
        ordem=nova_ordem,
        concluido=False,
        responsavel=u,
    )

    return JsonResponse({
        'success': True,
        'etapa': {
            'id': etapa.id,
            'descricao': etapa.etapa,
            'etapa_referencia': etapa.etapa_referencia,
            'ordem': etapa.ordem,
            'concluido': etapa.concluido,
            'responsavel': str(u),
        },
    })


@login_required
@require_POST
def excluir_etapa(request, etapa_id):
    """
    Endpoint AJAX para excluir uma Etapa (soft delete).
    """
    etapa = get_object_or_404(Etapa, pk=etapa_id)
    acao = etapa.acao

    # ── Verificar permissão ──
    u = request.user
    eh_assessor = (
        acao.responsavel_id
        and UserAssessor.objects.filter(
            titular_id=acao.responsavel_id,
            assessor_id=u.id,
        ).exists()
    )
    pode_editar = (
        u.is_superuser
        or getattr(u, 'admin', False)
        or getattr(u, 'gestor_chefe', False)
        or (acao.responsavel_id and acao.responsavel_id == u.id)
        or eh_assessor
    )
    if not pode_editar:
        return JsonResponse({'success': False, 'error': 'Permissão negada.'}, status=403)

    etapa.bl_deletado = True
    etapa.save()

    # Retorna o total de etapas ativas agora para atualizar o contador
    total_etapas = Etapa.objects.filter(acao=acao, bl_deletado=False).count()

    return JsonResponse({'success': True, 'total_etapas': total_etapas})


@login_required
@require_POST
def toggle_concluido_etapa(request, etapa_id):
    """
    Endpoint AJAX para marcar/desmarcar uma Etapa como concluída.
    """
    etapa = get_object_or_404(Etapa, pk=etapa_id)
    acao = etapa.acao

    # ── Verificar permissão ──
    u = request.user
    eh_assessor = (
        acao.responsavel_id
        and UserAssessor.objects.filter(
            titular_id=acao.responsavel_id,
            assessor_id=u.id,
        ).exists()
    )
    pode_editar = (
        u.is_superuser
        or getattr(u, 'admin', False)
        or getattr(u, 'gestor_chefe', False)
        or (acao.responsavel_id and acao.responsavel_id == u.id)
        or eh_assessor
    )
    if not pode_editar:
        return JsonResponse({'success': False, 'error': 'Permissão negada.'}, status=403)

    etapa.concluido = not etapa.concluido
    etapa.save()

    return JsonResponse({'success': True, 'concluido': etapa.concluido})
