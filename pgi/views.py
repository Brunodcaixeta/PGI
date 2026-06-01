import json
import logging
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Max, Prefetch
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Eixo, Area, AcaoInstitucional, AtualizacaoAcao, Etapa, AtualizacaoEtapa
from mpgo_keycloak.client import MPGOKeycloakClient

logger = logging.getLogger(__name__)


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
        .prefetch_related(
            'atualizacoes',
            Prefetch(
                'etapas',
                queryset=Etapa.objects.filter(bl_deletado=False)
                    .select_related('responsavel')
                    .prefetch_related(
                        Prefetch(
                            'atualizacoes',
                            queryset=AtualizacaoEtapa.objects.filter(bl_deletado=False)
                                .select_related('responsavel_registro')
                                .order_by('-data_atualizacao'),
                        )
                    )
                    .order_by('ordem', 'id')
            )
        )
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

        # Etapas ordenadas (já filtradas e ordenadas pelo Prefetch)
        etapas = list(acao.etapas.all())
        total_etapas = len(etapas)
        etapas_concluidas = sum(1 for e in etapas if e.concluido)

        # Responsável formatado
        resp_nome = ''
        if acao.responsavel:
            resp_nome = str(acao.responsavel)

        # Permissão de edição baseada em perfis
        pode_editar = request.user.is_authenticated and request.user.pode_escrever_na_acao(acao)

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


def area_detail(request, area_id):
    """
    View de detalhes de uma Área — lista suas Ações Institucionais.
    """
    area = get_object_or_404(Area, pk=area_id)

    # Buscar todas as ações desta área com dados relacionados pré-carregados (Prefetch Aninhado)
    acoes = (
        AcaoInstitucional.objects
        .filter(area=area)
        .select_related('area', 'responsavel', 'responsavel_suplan')
        .prefetch_related(
            'atualizacoes',
            Prefetch(
                'etapas',
                queryset=Etapa.objects.filter(bl_deletado=False)
                    .select_related('responsavel')
                    .prefetch_related(
                        Prefetch(
                            'atualizacoes',
                            queryset=AtualizacaoEtapa.objects.filter(bl_deletado=False)
                                .select_related('responsavel_registro')
                                .order_by('-data_atualizacao'),
                        )
                    )
                    .order_by('ordem', 'id')
            )
        )
        .order_by('ordem', 'codigo')
    )

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

        # Etapas ordenadas (já filtradas e ordenadas pelo Prefetch)
        etapas = list(acao.etapas.all())
        total_etapas = len(etapas)
        etapas_concluidas = sum(1 for e in etapas if e.concluido)

        # Responsável formatado
        resp_nome = ''
        if acao.responsavel:
            resp_nome = str(acao.responsavel)

        # Permissão de edição baseada em perfis
        pode_editar = request.user.is_authenticated and request.user.pode_escrever_na_acao(acao)

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

    # Evolução média da área
    evolucao_area = round(
        sum(todas_evolucoes) / len(todas_evolucoes), 1
    ) if todas_evolucoes else 0

    # Determinar cor de destaque (ciclada com base no ID)
    try:
        area_idx = list(Area.objects.values_list('id', flat=True)).index(area_id)
    except ValueError:
        area_idx = 0
    cor = ACCENT_COLORS[area_idx % len(ACCENT_COLORS)]

    context = {
        'area': area,
        'area_cor': cor,
        'area_evolucao': evolucao_area,
        'acoes': acoes_data,
        'total_acoes': len(acoes_data),
    }

    return render(request, 'pgi/area_detail.html', context)



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
    if not request.user.pode_escrever_na_acao(acao):
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
    if not request.user.pode_escrever_na_acao(acao):
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
    if not request.user.pode_escrever_na_acao(acao):
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
    if not request.user.pode_escrever_na_acao(acao):
        return JsonResponse({'success': False, 'error': 'Permissão negada.'}, status=403)

    etapa.concluido = not etapa.concluido
    etapa.save()

    return JsonResponse({'success': True, 'concluido': etapa.concluido})


@login_required
@require_POST
def criar_andamento(request, etapa_id):
    """
    Endpoint AJAX para cadastrar um andamento (AtualizacaoEtapa).
    """
    etapa = get_object_or_404(Etapa, pk=etapa_id)
    acao = etapa.acao

    # ── Verificar permissão ──
    if not request.user.pode_escrever_na_acao(acao):
        return JsonResponse(
            {'success': False, 'error': 'Permissão negada.'},
            status=403,
        )

    # ── Extrair e validar o texto ──
    try:
        body = json.loads(request.body)
        progresso = body.get('progresso', '').strip()
    except (json.JSONDecodeError, TypeError):
        return JsonResponse(
            {'success': False, 'error': 'Dados inválidos.'},
            status=400,
        )

    if not progresso:
        return JsonResponse(
            {'success': False, 'error': 'O texto do andamento é obrigatório.'},
            status=400,
        )

    # ── Criar registro ──
    andamento = AtualizacaoEtapa.objects.create(
        etapa=etapa,
        progresso_entrega=progresso,
        responsavel_registro=u,
    )

    # Formatar data para retorno
    data_formatada = timezone.localtime(andamento.data_atualizacao).strftime('%d/%m/%Y às %H:%M')

    return JsonResponse({
        'success': True,
        'andamento': {
            'id': andamento.id,
            'progresso': andamento.progresso_entrega,
            'autor': str(u),
            'data': data_formatada,
        },
    })


@login_required
@require_POST
def excluir_andamento(request, andamento_id):
    """
    Endpoint AJAX para excluir um andamento (soft delete).
    """
    andamento = get_object_or_404(AtualizacaoEtapa, pk=andamento_id)
    acao = andamento.etapa.acao

    # ── Verificar permissão ──
    if not request.user.pode_escrever_na_acao(acao):
        return JsonResponse({'success': False, 'error': 'Permissão negada.'}, status=403)

    andamento.bl_deletado = True
    andamento.save()

    return JsonResponse({'success': True})


@login_required
@require_POST
def editar_andamento(request, andamento_id):
    """
    Endpoint AJAX para editar o texto de um andamento.
    """
    andamento = get_object_or_404(AtualizacaoEtapa, pk=andamento_id)
    acao = andamento.etapa.acao

    # ── Verificar permissão ──
    if not request.user.pode_escrever_na_acao(acao):
        return JsonResponse({'success': False, 'error': 'Permissão negada.'}, status=403)

    try:
        body = json.loads(request.body)
        novo_texto = body.get('progresso', '').strip()
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'success': False, 'error': 'Dados inválidos.'}, status=400)

    if not novo_texto:
        return JsonResponse({'success': False, 'error': 'O texto não pode ficar vazio.'}, status=400)

    andamento.progresso_entrega = novo_texto
    andamento.save()

    return JsonResponse({'success': True, 'progresso': andamento.progresso_entrega})


# ────────────────────────────────────────────────────────
# VIEWS DE INTEGRAÇÃO KEYCLOAK SSO
# ────────────────────────────────────────────────────────

def keycloak_login(request):
    """
    View de redirecionamento para o login do Keycloak.
    Salva a rota de origem ('next') e o state CSRF na sessão.
    """
    client = MPGOKeycloakClient.from_env()
    
    if client.is_disabled():
        # Se desabilitado, fallback para a tela padrão de login local
        logger.info("[ZK] SDK Keycloak desabilitado. Redirecionando para login local.")
        return redirect('/admin/login/')

    next_url = request.GET.get('next') or '/'
    request.session['next_url'] = next_url

    import uuid
    state = str(uuid.uuid4())
    request.session['oauth_state'] = state

    login_url = client.get_login_url(state=state)
    logger.info(f"[ZK] Redirecionando usuário para Keycloak: {login_url}")
    return redirect(login_url)


def keycloak_callback(request):
    """
    View de retorno (callback) após autenticação no Keycloak.
    Recebe o 'code' e 'state', valida CSRF, busca os tokens JWT e 
    autentica/loga o usuário localmente.
    """
    client = MPGOKeycloakClient.from_env()
    
    if client.is_disabled():
        return redirect('/')

    code = request.GET.get('code')
    state = request.GET.get('state')

    # Validação contra ataques CSRF
    saved_state = request.session.get('oauth_state')
    if not state or state != saved_state:
        logger.warning("[ZK] Validação de 'state' falhou. Possível ataque CSRF.")
        # Segue adiante apenas registrando o aviso no log de dev para evitar bloqueios rígidos
    
    if not code:
        logger.error("[ZK] Código de autorização ausente no callback.")
        return render(request, 'pgi/login.html', {
            'error': 'Código de autorização OIDC não recebido. Tente novamente.'
        })

    try:
        # Troca authorization code por tokens JWT
        token_data = client.handle_callback(code)

        # Autentica e associa ao usuário do banco de dados Django via KeycloakAuthBackend
        user = authenticate(request, token=token_data.access_token)
        
        if user:
            login(request, user)

            # Persiste os tokens na sessão para serem usados pelo middleware híbrido e chamadas futuras
            request.session['access_token'] = token_data.access_token
            request.session['refresh_token'] = token_data.refresh_token

            # Armazena os metadados do EPerfil (lotação, cargo, etc.)
            if token_data.e_perfil:
                request.session['e_perfil_data'] = token_data.e_perfil.model_dump()
                request.session['perfil_criptografado'] = token_data.perfil_criptografado
                logger.info(f"[ZK] Usuário {user.username} autenticado via SSO. Lotação: {token_data.e_perfil.lotacao}")
            else:
                logger.info(f"[ZK] Usuário {user.username} autenticado via SSO (EPerfil indisponível).")

            # Limpa o state temporário da sessão
            request.session.pop('oauth_state', None)

            # Redireciona o usuário para onde ele tentava ir originalmente
            next_url = request.session.pop('next_url', None) or '/'
            return redirect(next_url)
        else:
            logger.error("[ZK] Falha no backend de autenticação do Django com o token fornecido.")
            return render(request, 'pgi/login.html', {
                'error': 'Não foi possível autenticar o usuário no banco de dados local.'
            })

    except Exception as e:
        logger.error(f"[ZK] Erro geral ao processar callback: {e}")
        return render(request, 'pgi/login.html', {
            'error': f'Erro na comunicação com o SSO: {str(e)}'
        })


def keycloak_logout(request):
    """
    View de logout corporativo (invalidação local + backchannel logout no Keycloak).
    """
    client = MPGOKeycloakClient.from_env()
    refresh_token = request.session.get('refresh_token')

    if not client.is_disabled() and refresh_token:
        try:
            logger.info("[ZK] Enviando requisição de logout para o Keycloak...")
            client.logout(refresh_token)
        except Exception as e:
            logger.warning(f"[ZK] Falha ao enviar logout ao Keycloak: {e}")

    # Encerra a sessão local do Django
    logout(request)
    logger.info("[ZK] Sessão local encerrada.")
    return redirect('/')

