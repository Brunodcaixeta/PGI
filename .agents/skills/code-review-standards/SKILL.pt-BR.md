---
name: code-review-standards
description: Revisa código quanto a qualidade, segurança, testes e padrões do projeto (PEP 8, type hints, VERSION, Docker, funcoes.md). Use ao revisar pull requests, mudanças de código ou quando o usuário pedir revisão de código ou checagem de qualidade.
---

# Padrões de Revisão de Código

Aplicar este checklist ao revisar código. Reportar achados no formato de feedback abaixo.

## Checklist de revisão

### Correção e lógica

- [ ] Lógica correta e casos de borda tratados.
- [ ] Sem bugs óbvios ou condições de corrida.
- [ ] Tratamento de erros presente e consistente.

### Segurança

- [ ] Sem chaves, tokens ou segredos no código; usar `.env` ou variáveis de ambiente.
- [ ] Entrada do usuário sanitizada; sem SQL cru (usar placeholders).
- [ ] Pydantic ou equivalente para validação de entrada.

### Padrões de código

- [ ] Type hints e docstrings (estilo Google) em funções públicas.
- [ ] snake_case para variáveis/funções/arquivos; PascalCase para classes; UPPER_CASE para constantes.
- [ ] Funções com ~40 linhas no máximo; DRY e SRP respeitados.
- [ ] f-strings e logging (sem print em produção).
- [ ] Imports no topo; sem imports inline.

### Testes e qualidade

- [ ] Testes unitários para comportamento novo/alterado; `tests/` com `test_<modulo>.py`.
- [ ] Meta 80% de cobertura para código tocado.
- [ ] Verificações de versão: `VERSION` existe; UI ou `/version` exibe "versão:" (ou equivalente).

### Arquitetura e entrega

- [ ] Separação limpa (domínio, casos de uso, infraestrutura); sem lógica de negócio em controladores.
- [ ] Repository / Service Layer quando aplicável; sem dependências circulares.
- [ ] `funcoes.md` atualizado se funções foram adicionadas, alteradas ou removidas.
- [ ] Código formatado (ex.: Black, Ruff); Conventional Commits se aplicável.

### DevOps e configuração

- [ ] Dockerfile e docker-compose (e variante app-only) se o projeto usar Docker.
- [ ] `.env.example` documenta variáveis necessárias.
- [ ] Sem dependências globais ou cache commitados.

## Formato de feedback

Classificar cada achado como:

- **Crítico**: Corrigir antes do merge (segurança, correção, bloqueante).
- **Sugestão**: Deve melhorar (legibilidade, performance, consistência).
- **Nice to have**: Melhoria opcional.

Manter o feedback concreto: citar arquivo/linha ou escopo e, quando possível, sugerir correção ou padrão.
