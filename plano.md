# Plano de Implementação — Módulo PGI

Este documento mapeia as tarefas de implementação técnica (Fases 3 e 4). Conforme implementado, marque com `[x]`.

## Fase 3 — Detalhamento por Área (Visão de Áreas)
*Página semelhante aos detalhes de eixo, porém filtrada por Área de Atuação.*

- [ ] Criar a rota URL `/area/<int:area_id>/` apontando para a view `area_detail` em `pgi/urls.py`.
- [ ] Implementar a view `area_detail` em `pgi/views.py`:
  - [ ] Buscar a Área (`get_object_or_404`).
  - [ ] Buscar as Ações vinculadas a esta área.
  - [ ] Aplicar `select_related` (eixo, responsavel) e `prefetch_related` (atualizacoes, etapas).
  - [ ] Calcular a evolução percentual da área e de cada ação.
- [ ] Criar o template `pgi/templates/pgi/area_detail.html`:
  - [ ] Replicar o cabeçalho com botão "Voltar".
  - [ ] Replicar a lista de ações com barra de progresso.
  - [ ] Replicar o painel expansível de etapas via JS.
- [ ] Atualizar o componente `card_area.html` para que o link aponte para a nova página (usando `{% url 'pgi:area_detail' area.id %}`).
- [ ] Testar navegação Home -> Toggle Áreas -> Detalhes da Área.

## Fase 4 — Formulário de Atualização de Progresso
*Interface para que os responsáveis editem livremente o percentual de execução das ações.*

- [ ] (Análise/Backend) Definir se a atualização de progresso ficará num Modal (na página detail) ou em uma tela separada.
- [ ] Criar endpoint POST / view para salvar o novo registro em `AtualizacaoAcao` vinculado à ação:
  - Validar entradas (garantir que seja entre 0 e 100, ou 0.0 e 1.0).
  - Validar permissões (somente o responsável logado pode editar? Ou todos os admins?).
- [ ] Criar interface (botão "Atualizar" ou input inline) no card da Ação dentro de `eixo_detail.html` e `area_detail.html`.
- [ ] Tratar erro/sucesso visualmente para o usuário.
- [ ] Escrever/atualizar testes automatizados se houver tempo.
