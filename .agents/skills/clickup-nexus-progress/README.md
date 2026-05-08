# clickup-nexus-progress

![Cursor Skill](https://img.shields.io/badge/Cursor-Skill-00d4aa?style=flat) ![MCP](https://img.shields.io/badge/MCP-ClickUp-7b68ee?style=flat) ![Markdown](https://img.shields.io/badge/doc-Markdown-083fa1?style=flat)

Read in Portuguese: [README.pt-BR.md](README.pt-BR.md)

Project skill to track **progress** and support **planning** of the **Nexus** app directly in **ClickUp** via the `user-clickup` MCP. Every task or comment includes the **module/file and function** in focus.

## When to use

- **Status / progress**: “show progress”, “what’s in progress”, “blockers”
- **Planning / roadmap**: “plan feature X”, “create backlog”, “prioritize”, “break down into tasks”
- **ClickUp sync**: “create/update tasks”, “post daily status”, “record evidence”

## Mandatory rule

Whenever creating, updating, or commenting in ClickUp, include this block:

```markdown
### Contexto técnico (obrigatório)
- App: Nexus
- Módulo/arquivo: `<path/to/file>`
- Função/classe: `<name>`
- Escopo: `<one sentence>`
- Evidência: `<link/commit/PR> (if any)`
```

If not yet known: set **Módulo/arquivo** and **Função/classe** to `não identificado ainda`.

## Supported flows

- **View progress**: find Nexus tasks/docs with `clickup_search`; summarize **in progress**, **blockers**, **next**; optionally post “status of the day” via `clickup_create_task_comment`.
- **Plan new features**: normalize the request; break down into parent task + subtasks; create/update tasks with `clickup_create_task` / `clickup_update_task`.

## Task name conventions

- `FEAT - ...` · `FIX - ...` · `TECH - ...` · `CHORE - ...`

## MCP tools used

`clickup_search` · `clickup_get_list` (resolve `list_id`) · `clickup_create_task` / `clickup_update_task` · `clickup_create_task_comment`

## Full instructions

See [SKILL.md](SKILL.md) for full rules and flows.
