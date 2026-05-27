# Funções e Views do Projeto PGI

Este arquivo documenta as principais funções e views criadas no projeto **Plano de Gestão Institucional (PGI)**, especificando seus propósitos, parâmetros, retornos e localizações.

---

## Módulo pgi (Views)

### home
- **Arquivo**: `pgi/views.py`
- **Propósito**: Renderiza a página inicial (dashboard global) contendo o progresso geral, a barra de evolução do triênio, os cards de Eixos Estratégicos e os cards de Áreas de Atuação.
- **Parâmetros**: 
  - `request`: Objeto de requisição HTTP do Django.
- **Retorno**: Renderização do template `pgi/home.html` com o contexto do dashboard.

### eixo_detail
- **Arquivo**: `pgi/views.py`
- **Propósito**: Exibe o detalhamento de um Eixo Estratégico específico, listando suas ações institucionais, progresso, etapas e timelines de andamentos, com checagem de permissão de edição.
- **Parâmetros**:
  - `request`: Objeto de requisição HTTP do Django.
  - `eixo_id` (int): Identificador (ID) do Eixo Estratégico.
- **Retorno**: Renderização do template `pgi/eixo_detail.html` com os dados do Eixo e ações pré-carregadas via *Prefetch Aninhado*.

### area_detail
- **Arquivo**: `pgi/views.py`
- **Propósito**: Exibe o detalhamento de uma Área de Atuação específica, listando todas as ações institucionais vinculadas, progresso, etapas de execução e timelines de andamentos, com as mesmas interatividades do eixo.
- **Parâmetros**:
  - `request`: Objeto de requisição HTTP do Django.
  - `area_id` (int): Identificador (ID) da Área de Atuação.
- **Retorno**: Renderização do template `pgi/area_detail.html` com os dados da Área e ações pré-carregadas.

### atualizar_evolucao
- **Arquivo**: `pgi/views.py`
- **Propósito**: Endpoint AJAX para atualizar o percentual de evolução/progresso de uma Ação Institucional específica.
- **Parâmetros**:
  - `request`: Objeto de requisição HTTP.
  - `acao_id` (int): ID da Ação Institucional a ser atualizada.
- **Retorno**: `JsonResponse` contendo o status da operação (`success`) e o novo valor de evolução.

### criar_etapa
- **Arquivo**: `pgi/views.py`
- **Propósito**: Endpoint AJAX para cadastrar uma nova Etapa de execução sob uma Ação Institucional específica.
- **Parâmetros**:
  - `request`: Objeto de requisição HTTP.
  - `acao_id` (int): ID da Ação sob a qual a etapa será criada.
- **Retorno**: `JsonResponse` contendo o status, detalhes da nova etapa (id, nome, responsável) ou mensagens de erro.

### excluir_etapa
- **Arquivo**: `pgi/views.py`
- **Propósito**: Endpoint AJAX para realizar a exclusão lógica (*soft delete*) de uma Etapa de execução.
- **Parâmetros**:
  - `request`: Objeto de requisição HTTP.
  - `etapa_id` (int): ID da Etapa a ser excluída.
- **Retorno**: `JsonResponse` indicando sucesso ou erro de permissão.

### toggle_concluido_etapa
- **Arquivo**: `pgi/views.py`
- **Propósito**: Endpoint AJAX para alternar o status de conclusão (concluído/pendente) de uma Etapa.
- **Parâmetros**:
  - `request`: Objeto de requisição HTTP.
  - `etapa_id` (int): ID da Etapa a ter o status alterado.
- **Retorno**: `JsonResponse` contendo o novo status de conclusão (`concluido`).

### criar_andamento
- **Arquivo**: `pgi/views.py`
- **Propósito**: Endpoint AJAX para cadastrar um novo andamento (registro de timeline) sob uma Etapa de execução específica.
- **Parâmetros**:
  - `request`: Objeto de requisição HTTP (com corpo em JSON).
  - `etapa_id` (int): ID da Etapa associada.
- **Retorno**: `JsonResponse` contendo o andamento criado formatado com autor, data e texto ou erro.

### excluir_andamento
- **Arquivo**: `pgi/views.py`
- **Propósito**: Endpoint AJAX para realizar a exclusão lógica (*soft delete*) de um andamento.
- **Parâmetros**:
  - `request`: Objeto de requisição HTTP.
  - `andamento_id` (int): ID do andamento a ser excluído.
- **Retorno**: `JsonResponse` indicando o sucesso da operação.

### editar_andamento
- **Arquivo**: `pgi/views.py`
- **Propósito**: Endpoint AJAX para editar o texto/conteúdo de um andamento existente.
- **Parâmetros**:
  - `request`: Objeto de requisição HTTP (com corpo em JSON contendo o novo texto).
  - `andamento_id` (int): ID do andamento a ser editado.
- **Retorno**: `JsonResponse` indicando sucesso e o texto atualizado.
