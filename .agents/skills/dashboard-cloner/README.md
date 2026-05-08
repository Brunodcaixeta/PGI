# Dashboard UI Cloner - Guide & Installation

[**Português (Portuguese)**](./README.pt-BR.md)

This directory contains a Skill for deep UI/UX analysis of dashboard screenshots to facilitate high-fidelity redevelopment.

## 🚀 How to use in new projects

### 1. In Antigravity (Claude Code / Gemini CLI)
To use this skill in a specific project:

1. Go to your project's root.
2. Create the `.agents/skills` directory.
3. Create a symbolic link:
   ```bash
   ln -s /Users/dms/Documents/source/ia_skills/dashboard-cloner $(pwd)/.agents/skills/dashboard-cloner
   ```

### 2. Usage Instructions
Simply provide a screenshot of a dashboard or UI and say:
- "Analyze this dashboard for a rebuild."
- "Clone this UI for me."
- "Extract design tokens from this screenshot."

The AI will output a structured **JSONC** document and a final **Developer Brief** prompt.

## 🛠️ Maintenance
Modify files in `/Users/dms/Documents/source/ia_skills/dashboard-cloner` to reflect improvements in analysis logic or output format.
