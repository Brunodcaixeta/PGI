# clickup-nexus-progress

![Cursor Skill](https://img.shields.io/badge/Cursor-Skill-00d4aa?style=flat) ![MCP](https://img.shields.io/badge/MCP-ClickUp-7b68ee?style=flat) ![Markdown](https://img.shields.io/badge/doc-Markdown-083fa1?style=flat)

Leia em inglês: [README.md](README.md)

Skill de projeto para acompanhar **andamento** e suportar **planejamento** do app **Nexus** diretamente no **ClickUp**, usando o MCP `user-clickup`. Toda tarefa ou comentário deve indicar **módulo/arquivo e função** em foco.

## Quando usar

- **Status/progresso**: “mostra o andamento”, “o que está em progresso”, “quais bloqueios”
- **Planejamento/roadmap**: “planeja a feature X”, “cria backlog”, “prioriza”, “decompõe em tarefas”
- **Sincronização com ClickUp**: “cria/atualiza tarefas”, “comenta status do dia”, “registra evidências”

## Regra principal (obrigatória)

Sempre que criar/atualizar/comentar algo no ClickUp, incluir:

```markdown
### Contexto técnico (obrigatório)
- App: Nexus
- Módulo/arquivo: `<caminho/do/arquivo>`
- Função/classe: `<nome>`
- Escopo: `<1 frase>`
- Evidência: `<link/commit/PR> (se houver)`
```

Se ainda não der para inferir: **Módulo/arquivo** e **Função/classe** = `não identificado ainda`.

## Fluxos suportados

- **Ver andamento**: localizar tarefas/docs do Nexus com `clickup_search`; sintetizar **em progresso**, **bloqueios**, **próximos**; quando apropriado, registrar “status do dia” via `clickup_create_task_comment`.
- **Planejar novas funcionalidades**: normalizar demanda; decompor em épico/tarefa-mãe + subtarefas; materializar no ClickUp com `clickup_create_task` / `clickup_update_task`.

## Convenções para nomes de tarefas

- `FEAT - ...` · `FIX - ...` · `TECH - ...` · `CHORE - ...`

## Ferramentas do MCP mais usadas

`clickup_search` · `clickup_get_list` (resolver `list_id`) · `clickup_create_task` / `clickup_update_task` · `clickup_create_task_comment`

## Instruções completas

Ver [SKILL.md](SKILL.md) para regras e fluxos completos.
