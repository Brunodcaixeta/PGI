# Django Technical Audit - Guia de Uso e Instalação

[English](./README.md)

Este diretório contém uma Skill para auditoria técnica de projetos Django.

## 🚀 Como usar em novos projetos

### 1. No Antigravity (Claude Code / Gemini CLI)
Para que o Antigravity reconheça esta skill em um novo projeto Django:

1. Vá para a raiz do seu novo projeto.
2. Crie a estrutura de pastas necessária:
   ```bash
   mkdir -p .agents/skills
   ```
3. Crie um link simbólico para esta pasta (recomendado para manter atualizado):
   ```bash
   ln -s /Users/dms/Documents/source/ia_skills/django-audit $(pwd)/.agents/skills/django-audit
   ```
4. O Antigravity passará a listar `django-audit` ao rodar em seu projeto.

---

### 2. No Cursor (IDE)
O Cursor utiliza o arquivo `.cursorrules` para definir comportamentos globais.

1. Na raiz do seu projeto no Cursor, crie ou abra o arquivo `.cursorrules`.
2. Copie e cole o conteúdo do arquivo `SKILL.md` (deste diretório) para dentro do seu `.cursorrules`.
3. Certifique-se de que o script `scripts/audit_check.py` também esteja disponível no projeto se desejar rodar as verificações automáticas.

---

### 3. Requisitos
- **Python 3.13+** (recomendado via Homebrew).
- Ferramentas de auditoria (instaladas automaticamente pelo script no primeiro uso dentro do `.audit_venv`).

## 🛠️ Manutenção
Para atualizar o script de auditoria ou regras, modifique os arquivos diretamente nesta pasta `/Users/dms/Documents/source/ia_skills/django-audit`. Todos os projetos que usarem o link simbólico serão atualizados simultaneamente.
