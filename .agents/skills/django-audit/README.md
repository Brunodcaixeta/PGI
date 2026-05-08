# Django Technical Audit - Guide & Installation

[**Português (Portuguese)**](./README.pt-BR.md)

This directory contains a Skill for technical auditing of Django projects.

## 🚀 How to use in new projects

### 1. In Antigravity (Claude Code / Gemini CLI)
To make Antigravity recognize this skill in a new Django project:

1. Go to the root of your new project.
2. Create the necessary folder structure:
   ```bash
   mkdir -p .agents/skills
   ```
3. Create a symbolic link to this folder (recommended for keeping it updated):
   ```bash
   ln -s /Users/dms/Documents/source/ia_skills/django-audit $(pwd)/.agents/skills/django-audit
   ```
4. Antigravity will now list `django-audit` when running in your project.

---

### 2. In Cursor (IDE)
Cursor uses the `.cursorrules` file to define global behaviors.

1. In the root of your project in Cursor, create or open the `.cursorrules` file.
2. Copy and paste the content of the `SKILL.md` file (from this directory) into your `.cursorrules`.
3. Ensure the `scripts/audit_check.py` script is also available in the project if you wish to run automatic checks.

---

### 3. Requirements
- **Python 3.13+** (recommended via Homebrew).
- Audit tools (automatically installed by the script on first use within `.audit_venv`).

## 🛠️ Maintenance
To update the audit script or rules, modify the files directly in this folder `/Users/dms/Documents/skills-claude/django-audit`. All projects using the symbolic link will be updated simultaneously.
