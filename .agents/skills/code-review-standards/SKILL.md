---
name: code-review-standards
description: Reviews code for quality, security, tests, and project standards (PEP 8, type hints, VERSION, Docker, funcoes.md). Use when reviewing pull requests, code changes, or when the user asks for a code review or quality check.
---

# Code Review Standards

Apply this checklist when reviewing code. Report findings in the feedback format below.

## Review checklist

### Correctness and logic

- [ ] Logic is correct and edge cases are handled.
- [ ] No obvious bugs or race conditions.
- [ ] Error handling is present and consistent.

### Security

- [ ] No keys, tokens, or secrets in code; use `.env` or environment variables.
- [ ] User input is sanitized; no raw SQL (use placeholders).
- [ ] Pydantic or equivalent used for input validation.

### Code standards

- [ ] Type hints and docstrings (Google style) on public functions.
- [ ] snake_case for variables/functions/files; PascalCase for classes; UPPER_CASE for constants.
- [ ] Functions under ~40 lines; DRY and SRP respected.
- [ ] f-strings and logging (no print for production).
- [ ] Imports at top; no inline imports.

### Tests and quality

- [ ] Unit tests for new/changed behavior; `tests/` with `test_<module>.py`.
- [ ] Target 80% coverage for touched code.
- [ ] Version checks: `VERSION` exists; UI or `/version` shows "versão:" (or equivalent).

### Architecture and delivery

- [ ] Clean separation (domain, use cases, infrastructure); no business logic in controllers.
- [ ] Repository / Service Layer where applicable; no circular dependencies.
- [ ] `funcoes.md` updated if functions were added, changed, or removed.
- [ ] Code formatted (e.g. Black, Ruff); Conventional Commits if applicable.

### DevOps and config

- [ ] Dockerfile and docker-compose (and app-only variant) if the project uses Docker.
- [ ] `.env.example` documents required variables.
- [ ] No global deps or cache committed.

## Feedback format

Classify each finding as:

- **Critical**: Must fix before merge (security, correctness, blocking).
- **Suggestion**: Should improve (readability, performance, consistency).
- **Nice to have**: Optional improvement.

Keep feedback concrete: cite file/line or scope and, when possible, suggest a fix or pattern.
