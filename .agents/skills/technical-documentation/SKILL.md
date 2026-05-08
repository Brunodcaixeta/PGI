---
name: technical-documentation
description: Creates and maintains analise.md and plano.md for technical discussions and implementation planning. Use when starting a technical discussion, planning implementation, or when the user asks for analysis documentation or a plan.
---

# Technical Documentation

Maintains two project artifacts: `analise.md` (technical analysis) and `plano.md` (implementation plan). Create or update them during technical discussions or when the user asks for analysis or plan documentation.

## analise.md

- **Purpose**: Record critical points, decisions, and Q&A from technical discussions.
- **Format**: Markdown with clear headings and separators.
- **Contents**: Key decisions, trade-offs, open questions, and answers.
- **When**: Create at the start of a technical discussion; update as decisions are made.

## plano.md

- **Purpose**: List small, concrete tasks to support implementation and rollback.
- **Format**: Markdown; checklist-style items.
- **Contents**: Tasks derived from `analise.md`, `funcoes.md`, and other project docs.
- **When**: Create after or with analysis; update as tasks are completed or changed.

## Workflow

1. **Starting a technical discussion**: Create or open `analise.md`; note scope and main questions.
2. **As decisions are made**: Update `analise.md` with decisions and rationale.
3. **Planning implementation**: Create or update `plano.md` with actionable tasks.
4. **As work progresses**: Check off or adjust items in `plano.md`.

Keep both files at project root. Use consistent Markdown (headings, lists, code blocks) and avoid duplicating long content; reference other docs instead.
