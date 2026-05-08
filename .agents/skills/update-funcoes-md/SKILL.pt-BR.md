---
name: update-funcoes-md
description: Mantém o arquivo funcoes.md do projeto atualizado quando funções forem criadas, alteradas ou removidas. Use após adicionar ou modificar uma função, ou quando o usuário pedir documentar funções ou atualizar funcoes.md.
---

# Atualizar funcoes.md

O arquivo `funcoes.md` na raiz do projeto deve listar e explicar brevemente cada função criada no projeto. Atualizá-lo sempre que uma função for adicionada, alterada ou removida.

## Quando atualizar

- **Nova função**: Adicionar entrada com nome, propósito, parâmetros, retorno e local (módulo/caminho).
- **Função alterada**: Atualizar a entrada existente para refletir o novo comportamento/assinatura.
- **Função removida**: Remover ou marcar a entrada como removida para manter a lista precisa.

## O que registrar por função

- **Nome** e **local** (arquivo/módulo).
- **Propósito**: O que faz em uma ou duas frases.
- **Parâmetros**: Nomes e papéis (e tipos se relevante).
- **Retorno**: Significado e tipo se relevante.
- **Notas**: Efeitos colaterais, exceções ou detalhes de uso importantes (opcional).

## Formato

Usar Markdown. Preferir estrutura simples, ex.:

```markdown
## modulo_ou_area

### nome_da_funcao
- **Arquivo**: path/to/file.py
- **Propósito**: ...
- **Parâmetros**: ...
- **Retorno**: ...
```

Ou tabela compacta se o projeto já usar. Manter terminologia consistente com a base de código.

## Regras

- Priorizar reuso de funções existentes antes de adicionar novas; documentar o reuso na entrada relevante se útil.
- Cada versão da função que altere comportamento deve ser refletida em `funcoes.md`.
- Considerar null safety e exceções documentadas onde importarem para quem chama.

Se `funcoes.md` não existir, criá-lo na raiz do projeto com uma breve introdução e depois adicionar as entradas.
