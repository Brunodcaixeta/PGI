
# 🧩 **Design System — UI**

*Versão 1.0 — Especificação Oficial de Interface*

---

# 1️⃣ Identidade Visual

## **Resumo**

O estilo visual do sistema segue o padrão:

* **Dark Mode First**
* **Enterprise / Modern Dashboard** (inspirado em Vercel, Linear, ShadCN)
* **Glassmorphism leve** em superfícies superiores
* **Soft Shadows + Neo-morphism discreto**
* **Componentes arredondados e limpos**
* **Tipografia Inter**
* **Ícones Material Outlined**

---

# 2️⃣ Paleta de Cores

## 🎨 **Cores Principais**

| Token         | Hex       | Uso                               |
| ------------- | --------- | --------------------------------- |
| `primary`     | `#0ea5e9` | Ações principais, botões, links   |
| `secondary`   | `#0284c7` | Estados alternativos              |
| `accent-cyan` | `#22d3ee` | Destaques / elementos importantes |

---

## 🌑 **Cores de Fundo (Dark Mode)**

| Token             | Hex       | Uso                      |
| ----------------- | --------- | ------------------------ |
| `background-dark` | `#0f172a` | Fundo geral da aplicação |
| `surface-dark`    | `#1e293b` | Painéis, cards, sidebars |
| `surface-light`   | `#ffffff` | Modo claro (fallback)    |

---

## 🖤 **Cores de Texto**

| Token          | Hex       | Uso                          |
| -------------- | --------- | ---------------------------- |
| `text-light`   | `#f1f5f9` | Texto principal no dark mode |
| `text-muted`   | `#94a3b8` | Textos auxiliares            |
| `text-primary` | `#0ea5e9` | Ações, links, parciais       |

---

## 🟢 **Estados**

| Estado         | Cor       | Uso                  |
| -------------- | --------- | -------------------- |
| Sucesso        | `#22c55e` | Progresso, concluído |
| Aviso          | `#eab308` | Pendências           |
| Erro / Urgente | `#ef4444` | Alertas importantes  |
| Informação     | `#38bdf8` | Indicadores neutros  |

---

# 3️⃣ Tipografia

### **Fonte padrão:**

**Inter** (Google Fonts)

### **Hierarquia**

| Elemento      | Tamanho | Peso    |
| ------------- | ------- | ------- |
| Título 1 (H1) | 28–32px | 600–700 |
| Título 2 (H2) | 22–26px | 600     |
| Título 3 (H3) | 18–20px | 500–600 |
| Texto normal  | 14–16px | 400     |
| Labels / UI   | 12–14px | 500     |

### **Características**

* Alta legibilidade
* Entrelinha confortável
* Excelente para dashboards densos

---

# 4️⃣ Layout e Grid

## 🌐 **Grid base**

* **12 colunas** (Tailwind padrão)
* Gaps grandes: `gap-6`, `gap-8`
* Espaçamento interno amplo: `p-6`, `p-8`

## 📌 **Estrutura do Dashboard**

### 1. **Sidebar fixa**

* Largura: ~260px
* Scroll próprio
* Ícones + labels
* Seleção com `bg-primary/10`

### 2. **Top bar com blur**

* Altura: 64–72px
* `backdrop-blur-xl`
* Transparência leve
* Ícones alinhados à direita

### 3. **Painel principal**

* Cards de métricas no topo
* Tabela de dados no centro
* Widgets de agenda e notificações à direita

---

# 5️⃣ Componentes

A seguir: **descrição funcional + regras de estilo** para a IA gerar componentes idênticos.

---

## 🧱 5.1 Sidebar

**Características:**

* Fundo `surface-dark`
* Itens com `rounded-xl`
* Ícones Material
* Estados:

  * normal: `text-muted`
  * ativo: `bg-primary/10`, `text-primary`

**Anatomia:**

```
[ Ícone ] [ Label ]
```

---

## 🪟 5.2 Header (Top Bar)

**Características:**

* Vidro (glassmorphism)
* `backdrop-blur-xl`
* Fundo translúcido
* Campo de busca
* Ações: notificação, tema, conta do usuário

---

## 📊 5.3 Cards de Métricas

**Características:**

* `rounded-2xl`
* Cor dominante da métrica:

  * azul → geral
  * verde → progresso
  * amarelo → atrasos
* Ícone grande em segundo plano (`opacity-10`)
* Tipografia forte

**Anatomia:**

```
[ Ícone ]  Título
Valor Grande
Legenda / Detalhe
```

---

## 📑 5.4 Tabela (Planos Ativos)

**Características:**

* Cabeçalho com fundo escuro translúcido
* Linhas com hover leve
* Tags de status:

  * Em Execução → verde
  * Análise → azul
  * Atrasado → amarelo
* Barra de progresso simples (thin progress bar)

**Anatomia da Linha:**

```
[ Nome do plano ] [ Responsável ] [ Status ] [ Progresso ] [ Ações ]
```

---

## 📅 5.5 Agenda Prioritária

**Características:**

* `rounded-2xl`
* Destaque para data (dia/mês grande)
* Eventos organizados verticalmente
* Indicadores de urgência (vermelho)

---

## 🔔 5.6 Atualizações Recentes

**Características:**

* Painel menor com `shadow-glow`
* Ícone de informação
* Lista de notificações breves

---

# 6️⃣ Interações e Microcomportamentos

## ✨ Hover States

* Botões → brilho leve + mudança de cor
* Itens da tabela → `bg-white/5`
* Menu lateral → `bg-primary/10`

---

## 🌙 Tema (Dark/Light)

* Dark padrão
* Light ativado via `class="light"` na `<html>`
* Todos os tokens suportam variações (`dark:text-muted`, `dark:bg-surface-dark` etc.)

---

# 7️⃣ Componentes de Código (Tailwind Templates)

## 🔹 Button Primary

```html
<button class="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/80">
  Ação
</button>
```

## 🔹 Card Base

```html
<div class="rounded-2xl bg-surface-dark p-6 shadow-lg">
  <!-- conteúdo -->
</div>
```

## 🔹 Status Tag

```html
<span class="px-3 py-1 rounded-xl text-sm bg-green-500/20 text-green-400">
  Em Execução
</span>
```

---

# 8️⃣ Padrões de UX

* Informações priorizadas por importância visual
* Hierarquia clara de navegação
* Feedback visual imediato (cores + microanimações)
* Espaçamentos amplos para legibilidade
* Proporção 70% conteúdo / 30% painel lateral

---

# 9️⃣ Recomendações para IA de Programação

Inclua no prompt:

* “Gerar UI seguindo o Design System PromotorJud”
* “Utilizar TailwindCSS com dark mode e glassmorphism”
* “Sidebar fixa, header translúcido, cards com gráficos simples”
* “Utilizar Inter como fonte principal e Material Icons”
* “Respeitar tokens: primary, surface-dark, text-muted”

---

# 🔟 Conclusão

Este Design System oferece:

* consistência visual
* base sólida para IA gerar telas complexas
* escalabilidade para novos módulos
