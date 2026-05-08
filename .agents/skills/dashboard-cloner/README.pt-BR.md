# Dashboard UI Cloner - Guia de Uso e Instalação

[English](./README.md)

Este diretório contém uma Skill para análise profunda de UI/UX de screenshots de dashboards para facilitar a reconstrução de alta fidelidade.

## 🚀 Como usar em novos projetos

### 1. No Antigravity (Claude Code / Gemini CLI)
Para usar esta skill em um projeto específico:

1. Vá para a raiz do seu projeto.
2. Crie o diretório `.agents/skills`.
3. Crie um link simbólico:
   ```bash
   ln -s /Users/dms/Documents/source/ia_skills/dashboard-cloner $(pwd)/.agents/skills/dashboard-cloner
   ```

### 2. Instruções de Uso
Basta fornecer um screenshot de um dashboard ou UI e dizer:
- "Analise este dashboard para reconstrução."
- "Clone esta UI para mim."
- "Extraia os design tokens deste screenshot."

A IA entregará um documento **JSONC** estruturado e um prompt final focado no desenvolvedor (**Developer Brief**).

## 🛠️ Manutenção
Modifique os arquivos em `/Users/dms/Documents/source/ia_skills/dashboard-cloner` para refletir melhorias na lógica de análise ou no formato da saída.
