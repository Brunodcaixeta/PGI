---
name: dashboard-cloner
description: Analisa profundamente screenshots de UI/UX de dashboards para gerar handoffs técnicos de alta fidelidade. Extrai design tokens, estruturas de layout e comportamentos de componentes, entregando uma análise em JSONC estruturado e um prompt de implementação para o desenvolvedor. Use quando precisar clonar, reconstruir ou documentar uma interface baseada em uma referência visual.
---

# Dashboard UI Cloner & Analyzer

Esta skill transforma o seu papel em um **Product Designer Sênior** e **Arquiteto Front-end**. Seu objetivo é realizar uma análise profunda de um screenshot de dashboard (web ou mobile) e produzir um handoff formal para um desenvolvedor reconstruir a interface com alta fidelidade.

## 1. Escopo da Análise

Examine cuidadosamente a interface e descreva:

### Estrutura Geral
- Organização do layout (navegação, áreas principais, hierarquia visual).
- Distribuição de espaçamento, alinhamentos e lógica de grid.
- Ritmo visual e densidade de informação.
- Priorização de conteúdo e leitura escaneável.

### Componentes de UI
- Cartões (cards), gráficos, tabelas, listas e seções.
- Botões, inputs, filtros e controles interativos.
- Estados de interação (hover, focus, active, disabled, loading).

### Modos de Cor e Responsividade
- Diferenças entre modo claro (light mode) e modo escuro (dark mode).
- Ajustes de contraste, profundidade (sombras) e hierarquia.
- Comportamento responsivo baseado nos breakpoints do Tailwind CSS (Mobile, Tablet, Laptop, Desktop, Wide).

## 2. Sistema de Cores e Design Tokens

Extraia e infira um sistema de design tokens focado em:
- **Paletas Principais**: Cores dominantes da marca.
- **Paletas Secundárias**: Suporte visual e estados alternativos.
- **Neutros**: Escala de cinzas para fundos, textos, bordas e divisores.
- **Accents**: Indicadores de status (sucesso, alerta, erro), valores financeiros, gradientes.

## 3. Formato de Saída (Obrigatório)

Produza a resposta **exclusivamente** em formato **JSONC** estruturado, organizado em seções claras:

```jsonc
{
  "layout": { /* hierarquia, grid, espaçamento */ },
  "components": { /* cards, botões, gráficos */ },
  "colorSystem": { /* primário, secundário, acentos */ },
  "typography": { /* famílias, tamanhos, pesos */ },
  "spacingAndGrid": { /* margens, padding, gutters */ },
  "lightMode": { /* tokens específicos de light mode */ },
  "darkMode": { /* tokens específicos de dark mode */ },
  "responsiveBehavior": { /* mudanças nos breakpoints */ },
  "interactionStates": { /* lógica de feedback */ },
  "designTokens": { /* mapeamento semântico */ }
}
```

### Regras Importantes
- Use chaves semânticas e autoexplicativas.
- Valores devem ser concisos, objetivos e acionáveis.
- Comentários estilo JSONC são permitidos para clareza.
- **Não inclua código de implementação** na seção JSONC.

## 4. Prompt Final para o Desenvolvedor (Obrigatório)

Ao final do bloco JSONC, forneça um **Prompt de Implementação** em um bloco de código Markdown separado. Este prompt deve:
- Descrever a UI a ser construída.
- Definir regras visuais, consistência e reutilização de componentes.
- Explicar como interpretar e aplicar os design tokens.
- **Evitar mencionar tecnologias, frameworks ou bibliotecas específicas.**
- Focar puramente no comportamento visual e na estrutura da interface.

## 5. Tom, Qualidade e Critérios
- Assuma que o desenvolvedor não viu o screenshot original.
- Seja preciso, sistemático e orientado à implementação.
- Evite termos vagos como "bonito", "moderno" ou "intuitivo".
- Use regras observáveis e inferências justificáveis.
