---
name: django-audit
description: Realiza uma auditoria técnica completa de aplicações Django, cobrindo segurança, padrões de arquitetura, performance, banco de dados e qualidade de código. Use este skill sempre que precisar revisar um app Django em busca de bugs, riscos de segurança ou débitos técnicos.
---

# Django Technical Audit

Este skill orienta a realização de uma auditoria técnica rigorosa em aplicações Django, focando em segurança, padrões, performance e qualidade.

## Como Trabalhar

1. **Varredura**: Identifique os arquivos principais do diretório/app alvo (models, views, urls, forms/serializers, templates, admin, services, tests, migrations).
2. **Avaliação**: Leia e avalie arquivo por arquivo, apontando inconsistências com referência ao caminho e, quando possível, nome do método/classe.
3. **Classificação**: Classifique cada achado por **Severidade** (CRÍTICO, URGENTE, MÉDIO, BAIXO) e **Categoria** (Segurança, Bugs, Django best practices, Performance, DB, Testes, Arquitetura, Manutenibilidade, Observabilidade, DX/DevOps).
4. **Foco**: Foque em correções incrementais e seguras. Não invente arquivos.

## Checklist de Auditoria

### 1. Segurança (Obrigatório)
- **Autenticação e Autorização**: Verifique o uso de `@login_required`, `permission_required`, verificações de grupo, `user.is_staff`, `user.is_superuser`.
- **Exposição de Dados**: Verifique exposição de tokens, secrets, logs ou debug.
- **Vulnerabilidades**:
    - **SQL Injection**: Uso de `.extra()`, `raw()`, f-strings em SQL ou concatenação direta.
    - **XSS**: Templates sem escape ou uso indevido de filtro `safe`/`mark_safe`.
    - **CSRF**: Views desprotegidas em submissões de formulário.
- **Settings**: Verifique `DEBUG=True` em produção, `ALLOWED_HOSTS` genérico, falta de headers `SECURE_*`, cookies sem `Secure/HttpOnly/SameSite`.

### 2. Padrões Django e Arquitetura
- **Modelos**: Normalização, validações (`clean`), choices, constraints, indexes.
- **Views**: Separação de lógica (View vs Service/Layer), evitar lógica de negócio excessiva.
- **Forms/Serializers**: Validações adequadas.
- **Admin**: Permissões, `list_display`, `search_fields`.
- **Transações**: Uso de `transaction.atomic()` para operações que envolvem múltiplas tabelas.
- **Sinais (Signals)**: Evitar efeitos colaterais não controlados.

### 3. Performance e Banco de Dados
- **Queries N+1**: Falta de `select_related` ou `prefetch_related`.
- **Índices**: Ausência em FKs e campos de filtro frequentes.
- **Consultas**: Pesadas dentro de loops ou falta de paginação em listagens.

### 4. Testes e Qualidade
- **Cobertura**: Existência de testes para regras críticas e fluxos principais.
- **Segurança**: Testes para autorização e permissões.
- **Estilo**: PEP 8, docstrings, tratamento de exceções (evitar `except: pass`).

## Formato do Relatório (Entregável)

O relatório final deve ser em Markdown com a seguinte estrutura:

## 📌 Resumo Executivo
- 5 a 10 pontos principais focando em riscos CRÍTICO/URGENTE.

## ✅ Inventário Analisado
- Lista de diretórios e arquivos revisados (com paths).

## 🚨 Achados por Severidade

### CRÍTICO
- **[Categoria]** caminho/arquivo.py::ClasseOuFuncao
- **Impacto**: ...
- **Risco**: ...
- **Como corrigir**: Passos detalhados.
- **Teste sugerido**: Como validar a correção.

*(Repita para URGENTE, MÉDIO e BAIXO conforme necessário)*

## 🧪 Plano de Testes Recomendado
- Lista de testes novos a criar, agrupados por área.

## 🛠️ Correções Sugeridas (Priorizadas)
- Checklist ordenado do mais crítico ao menos crítico.

## 🧭 Próximos Passos
- Recomendações de melhoria incremental (refactor, padrões, tooling).

---

## 🛠️ Scripts Utilitários

O skill inclui um script para facilitar a execução de ferramentas de auditoria:

- `scripts/audit_check.py`: Roda verificações automáticas (Django deploy check, Bandit, Ruff, pip-audit).
  - **Automatização**: O script cria um ambiente virtual isolado (`.audit_venv`), instala ferramentas de auditoria e tenta instalar as dependências do projeto (`requirements.txt`) para uma análise completa e segura.
  - Uso: `python scripts/audit_check.py [app_dir]`
