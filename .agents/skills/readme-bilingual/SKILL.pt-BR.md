---
name: readme-bilingual
description: Cria e mantém READMEs duais (README.md em inglês, README.pt-BR.md em português) otimizados para o GitHub.com, com badges, links cruzados e imagens opcionais. Use ao criar ou atualizar documentação do projeto, quando o usuário pedir README ou documentação bilíngue, ou ao adicionar um novo app.
---

# README Bilíngue (EN + pt-BR)

Especialista em READMEs para apps em qualquer linguagem. A saída é **otimizada para o GitHub.com**: página inicial do repositório, descoberta e renderização Markdown. Sempre entregar **dois arquivos**: principal em inglês, adicional em português (pt-BR). Ser criativo (8/10), conciso e evitar repetição ou enchimento.

## Arquivos de saída

| Arquivo | Idioma | Papel no GitHub |
|---------|--------|-----------------|
| `README.md` | Inglês | **Página inicial do repositório** (landing padrão do repo) |
| `README.pt-BR.md` | Português (pt-BR) | Adicional; linkado a partir do README.md para o visitante trocar |

**Se já existir um README em português:** renomear/copiar para `README.pt-BR.md`, depois criar um novo `README.md` em inglês (não sobrescrever o conteúdo pt-BR existente).

## Link cruzado entre versões

O GitHub exibe apenas um README na home do repositório. Em **ambos** os arquivos, perto do topo (após o título ou badges), adicionar uma linha para o visitante abrir o outro idioma:

- No **README.md**:  
  `Read in Portuguese: [README.pt-BR.md](README.pt-BR.md)`
- No **README.pt-BR.md**:  
  `Leia em inglês: [README.md](README.md)`

Usar **caminhos relativos** para os links funcionarem no GitHub (sem URLs absolutas). Ajustar redação só se necessário para o tom.

## Badges

Usar badges **compatíveis com o GitHub** para renderizarem corretamente na página do repo. Preferir [Shields.io](https://shields.io): ex. licença, linguagem/runtime, status do GitHub Actions, release/versão, cobertura. Colocar sob o título; 3 a 6 badges. Quando o repo tiver Actions/workflows, incluir badge de status se relevante. Exemplo: `![CI](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)`.

## Imagens

O GitHub renderiza imagens do repositório por caminhos relativos. Se o projeto tiver **`images/`** ou **`docs/images/`** com assets relevantes (screenshot, logo, diagrama), incluir 1 a 2 com legenda curta. Usar caminhos como `images/screenshot.png` para funcionarem no GitHub. Se não houver pasta ou imagem relevante, omitir.

## Requisitos de conteúdo

- **O que o app faz**: Sempre incluir descrição curta e clara (1 a 3 frases) do que o aplicativo faz.
- **Seções**: Estrutura adequada ao GitHub (ex.: Description, Install, Usage, Config, Contributing, License). Usar headings e listas para a página ser escaneável. Ser breve; evitar parágrafos longos.
- **Tom**: Profissional, direto. Criatividade 8/10: redação variada, sem encheção de linguiça genérica, sem detalhes irrelevantes.
- **Links**: Preferir links relativos para arquivos do repo (ex. `[Contributing](CONTRIBUTING.md)`) para funcionarem no GitHub.

## Checklist antes de entregar

- [ ] Dois arquivos: `README.md` (EN) e `README.pt-BR.md` (pt-BR).
- [ ] Link cruzado presente em ambos; links relativos para o GitHub.
- [ ] Badges adicionadas (3 a 6), compatíveis com o GitHub e renderizando na página do repo.
- [ ] Descrição do app incluída em ambos.
- [ ] Imagens de `images/` ou `docs/images/` usadas se disponíveis; caminhos relativos.
- [ ] Conciso; sem repetição entre EN e pt-BR além da estrutura.
