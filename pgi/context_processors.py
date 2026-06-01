from pgi.models import AtualizacaoEtapa

def notificacoes_recentes(request):
    """
    Context processor para injetar as 5 atualizações de etapas mais recentes
    em todas as páginas do sistema para o sino de notificações.
    """
    if request.user.is_authenticated:
        # Pega as 5 últimas atualizações de etapas que não foram deletadas
        ultimas = (
            AtualizacaoEtapa.objects.filter(bl_deletado=False)
            .select_related('etapa__acao', 'responsavel_registro')
            .order_by('-data_atualizacao')[:5]
        )
        return {'notificacoes_recentes': ultimas}
    return {'notificacoes_recentes': []}
