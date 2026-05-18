# Análise Técnica — Módulo PGI

*Este documento registra as decisões arquiteturais, regras de negócio e pontos críticos discutidos e implementados durante o desenvolvimento.*

---

## 1. Banco de Dados e Infraestrutura

### Banco de Dados Local (Docker) vs VM de Produção
- **Decisão:** Durante a fase de desenvolvimento do front-end, optou-se por utilizar o banco de dados PostgreSQL 15 rodando localmente via Docker (definido em `docker-compose.yml`), em vez de conectar diretamente à VM de produção.
- **Motivo:** Garantir a integridade dos dados na VM de produção e evitar latência de rede (ou problemas de VPN/firewall) durante a compilação e teste intensivo do front-end.
- **Carga de Dados:** O banco foi populado com um script de migração a partir de arquivos CSV previamente limpos, garantindo que o ambiente de dev possua os mesmos dados (41 usuários, 78 ações e 642 etapas) para testar cálculos agregados e performance.

---

## 2. Front-end: Stack Tecnológica

### Tailwind CSS v4 (CLI Standalone)
- **Decisão:** Utilizar o Tailwind v4 via executável independente (Standalone CLI).
- **Motivo:** O projeto é desenvolvido num ambiente heterogêneo (macOS x86, macOS ARM e Windows). O uso do CLI standalone evita a dependência pesada de um ecossistema Node.js (`npm install`, `node_modules`).
- **Arquitetura de CSS:** No Tailwind v4, a configuração migrou do `tailwind.config.js` diretamente para o arquivo CSS (`input.css`) utilizando a diretiva `@theme`. Isso centralizou nossos tokens de design de forma muito mais coesa com o *UI Guide*.

### Arquitetura de Templates (Django)
- **Extensibilidade:** Utilizou-se o padrão `base.html` contendo `sidebar` e `header` injetados via `{% include %}`.
- **Componentização:** Padrão de pastas `components/` onde temos `card_eixo.html` e `card_area.html` que recebem o contexto via `{% include '...' with var=var %}`. Isso garantiu reuso de código nos grids.

---

## 3. Lógica de Negócio: Cálculos de Evolução

O banco de dados original registra a evolução em formato decimal (0.0 a 1.0). Para o front-end, isso é convertido para porcentagem (0% a 100%).

### Otimização de Consultas (N+1 Problem)
Para exibir o progresso de cada Eixo na tela inicial, é necessário saber o progresso da ação mais atual de cada uma das suas ações.
- **O Risco:** Se fizéssemos uma consulta ingênua (`acao.atualizacoes.all().first()`), o Django ORM faria uma query SQL no banco para *cada* ação carregada, resultando em mais de 78 consultas.
- **A Solução:** Utilizou-se `prefetch_related('atualizacoes')` e `select_related('responsavel')` nas views (`pgi/views.py`). O Django resolve tudo em 2 a 3 queries pesadas, e a ordenação da última atualização é feita em memória na camada Python (`sorted()`). Isso reduziu drasticamente o TTFB (Time to First Byte).

### Escala de Progresso
Na visualização detalhada (`eixo_detail.html`), adotamos uma escala de cores baseada na performance:
- Verde (`#22c55e`): Evolução $\ge 80\%$
- Amarelo (`#eab308`): Evolução $\ge 40\%$
- Azul (Cor do eixo): Evolução $< 40\%$

---

## 4. Problemas Resolvidos (Gotchas)

- **Recursão Infinita no Template Django:** Durante a montagem dos cards, deixou-se tags `{% include %}` comentadas com HTML puro (`<!-- -->`). O parser de template do Django continuava avaliando e executando as tags comentadas, levando a um `RecursionError` de limite de profundidade. A solução foi remover a tag ou usar `{% comment %}`.
- **Filtro Pluralize:** O Django espera a sintaxe `singular,plural`. Em português, para "Ação/Ações", é necessário usar: `Aç{{ num|pluralize:"ão,ões" }}`.

---

## 5. Próximos Passos (Backlog Técnico)

1. **Visão Detalhada de Áreas:** Criar a página `/area/<id>/` mapeada a partir do clique nos cards da Visão por Áreas na Home. A view reaproveitará a lógica e os componentes do `eixo_detail`.
2. **Atualização de Progresso (CRUD):** Implementar formulário/modal autenticado para que responsáveis pelas ações possam enviar um novo valor percentual livre (criando uma nova entrada em `AtualizacaoAcao`).
3. **Gerenciamento de CI/CD:** Quando a fase de dev local finalizar, configurar o workflow para deploy dos containers na VM Institucional.
