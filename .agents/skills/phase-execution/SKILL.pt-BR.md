---
name: phase-execution
description: Executa a entrega do projeto em cinco fases (análise, planejamento, implementação, validação, entrega) com checklists e relatório final estruturado. Use quando o usuário pedir executar uma fase, entregar a Fase 1, rodar entrega metodológica ou seguir execução por fases.
---

# Execução por Fases

Orienta a execução de uma fase do projeto (ex.: Fase 1) de forma controlada e rastreável. Executar **apenas** a fase solicitada; não avançar para fases posteriores.

## Workflow

Acompanhe o progresso com este checklist:

```
- [ ] Fase 1: Análise
- [ ] Fase 2: Planejamento
- [ ] Fase 3: Implementação
- [ ] Fase 4: Validação
- [ ] Fase 5: Entrega
```

### 1. Fase 1 — Análise (obrigatória primeiro)

- **Contexto**: Analisar escopo, objetivos e requisitos técnicos/funcionais.
- **Dependências**: Identificar ligações com fases futuras.
- **Impacto**: Avaliar decisões arquiteturais que afetam tarefas posteriores.
- **Validação**: Confirmar entendimento técnico e funcional antes de iniciar.

### 2. Fase 2 — Planejamento

- **Estratégia**: Definir a abordagem técnica mais adequada.
- **Estrutura**: Planejar organização de código e recursos.
- **Riscos**: Identificar possíveis falhas e medidas preventivas.

### 3. Fase 3 — Implementação

- Implementar todos os componentes necessários à fase.
- Aplicar padrões do projeto (validações, tratamento de erros, null safety).
- Otimizar PostgreSQL (índices, constraints, transações).
- Configurar FastAPI, logging, monitoramento.
- Incluir testes unitários (cobertura mínima 80%).
- Atualizar README, diagramas e documentação técnica.

### 4. Fase 4 — Validação

- **Testes funcionais**: Verificar se todos os requisitos da fase foram atendidos.
- **Testes de integração**: Validar PostgreSQL e serviços externos.
- **Revisão de código**: Executar checklist de qualidade antes da entrega.

### 5. Fase 5 — Entrega

- Produzir checklist detalhado dos itens implementados.
- Atualizar status no formato abaixo.
- Produzir o relatório final (template abaixo).

## Formato de atualização de status

Use este template para status antes/depois:

```markdown
# Antes da execução
- [ ] Item 1
- [ ] Item 2

# Após a execução
- [x] Item 1
- [x] Item 2
```

## Restrições

- **Foco**: Executar APENAS a fase solicitada; não iniciar a próxima.
- **Consciência**: Manter em mente o impacto nas fases futuras.
- **Qualidade**: Não sacrificar qualidade por velocidade.
- **Conclusão**: Finalizar 100% da fase antes de reportar.

## Padrões de qualidade (durante a implementação)

- **Python**: PEP 8, type hints, docstrings.
- **PostgreSQL**: Otimizar queries, índices, constraints.
- **FastAPI**: Validação Pydantic, response models, documentação.
- **Arquitetura**: Separar responsabilidades, injeção de dependências, logging.

## Template do relatório final

Entregar relatório com:

1. **Resumo executivo**: O que foi implementado e como.
2. **Checklist de conclusão**: Lista detalhada de itens finalizados.
3. **Arquivos atualizados**: Confirmação das atualizações de status.
4. **Observações técnicas**: Decisões arquiteturais relevantes para fases futuras.
5. **Próximos passos**: Recomendações para a próxima fase (não executá-los).
