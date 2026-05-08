---
name: technical-documentation
description: Cria e mantém analise.md e plano.md para discussões técnicas e planejamento de implementação. Use ao iniciar discussão técnica, planejar implementação ou quando o usuário pedir documentação de análise ou plano.
---

# Documentação Técnica

Mantém dois artefatos do projeto: `analise.md` (análise técnica) e `plano.md` (plano de implementação). Criar ou atualizar durante discussões técnicas ou quando o usuário pedir documentação de análise ou plano.

## analise.md

- **Propósito**: Registrar pontos críticos, decisões e perguntas/respostas das discussões técnicas.
- **Formato**: Markdown com headings e separadores claros.
- **Conteúdo**: Decisões principais, trade-offs, perguntas em aberto e respostas.
- **Quando**: Criar no início da discussão técnica; atualizar conforme decisões forem tomadas.

## plano.md

- **Propósito**: Listar tarefas pequenas e concretas para implementação e rollback.
- **Formato**: Markdown; itens em estilo checklist.
- **Conteúdo**: Tarefas derivadas de `analise.md`, `funcoes.md` e outros docs do projeto.
- **Quando**: Criar após ou junto com a análise; atualizar conforme tarefas forem concluídas ou alteradas.

## Workflow

1. **Iniciando discussão técnica**: Criar ou abrir `analise.md`; anotar escopo e principais perguntas.
2. **Conforme decisões forem tomadas**: Atualizar `analise.md` com decisões e justificativas.
3. **Planejando implementação**: Criar ou atualizar `plano.md` com tarefas acionáveis.
4. **Conforme o trabalho avança**: Marcar ou ajustar itens em `plano.md`.

Manter ambos os arquivos na raiz do projeto. Usar Markdown consistente (headings, listas, blocos de código) e evitar duplicar conteúdo longo; referenciar outros docs.
