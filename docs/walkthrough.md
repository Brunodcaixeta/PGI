# Walkthrough: Reformulação de Permissões & Melhorias de Interface (Frontend)

O desenvolvimento da reformulação de perfis, controle de acesso e todas as melhorias visuais e funcionais de interface do PGI foi concluído com sucesso. 

Abaixo está o resumo dos recursos desenvolvidos, testados e validados no projeto.

---

## Recursos Implementados

### 1. Novo Controle de Acesso por Perfis (Local e Seguro)
- **4 Perfis Clariificados:** Eliminamos a tabela complexa de assessores e estruturamos o acesso nas regras de negócio da instituição:
  - **`adm`:** Acesso total de escrita e controle de usuários no admin.
  - **`gestor`:** Acesso total de escrita nas ações/etapas por meio das telas principais (home/detalhes), sem privilégios administrativos de usuários.
  - **`editor`:** Acesso restrito de escrita **exclusivamente** nas ações associadas à sua respectiva **Área** (ex: *SUPLAN*).
  - **`leitor`:** Visualizador comum, apenas leitura de evoluções, etapas e andamentos, sem botões de escrita visíveis.
- **Sincronização na Importação:** O script `importar_dados` mapeia de forma inteligente as colunas legadas e vincula automaticamente os usuários às suas respectivas áreas baseando-se nas ações/etapas sob sua responsabilidade, promovendo-os para `editor`.

### 2. Notificações Recentes no Sino (Cabeçalho)
- Criamos um **Context Processor** do Django que consulta globalmente as 5 últimas atualizações de etapas (`AtualizacaoEtapa`) ativas no banco de dados.
- Mapeamos o sino de notificações para servir de gatilho para um **Dropdown de Notificações Popover** com efeito de vidro translúcido (*glassmorphism*). Ele exibe quem realizou a atualização, qual o texto do andamento, a sigla da ação e a data/hora exata.
- Um badge vermelho discreto é exibido no topo do sino se houver atividades recentes não visualizadas.

### 3. Atalho e Modal de Configurações (Sidebar)
- O botão **Configurações** na sidebar foi habilitado com inteligência de perfil:
  - Se um **Administrador (`adm`)** ou superusuário clicar, ele é redirecionado de forma imediata para o painel de gerenciamento de usuários do Django Admin (`/admin/pgi/user/`).
  - Se um **Editor, Gestor ou Leitor** clicar, abre-se um modal flutuante com efeito glassmorphic exibindo de forma clara suas informações de conta (Nome Completo, E-mail, Matrícula, Perfil de Acesso do PGI e sua respectiva Área de Lotação).

### 4. Filtro Instantâneo de Busca Robustecido e Expandido para a Home
- A barra de pesquisa no topo direito ganhou vida. Implementamos um script em JavaScript no arquivo `base.html` que intercepta a digitação em tempo real e funciona em múltiplos contextos:
  - **Nas Telas de Detalhes (`eixo_detail` e `area_detail`):** Pesquisa e filtra instantaneamente os cards de ações `.acao-card` por qualquer conteúdo de texto (como descrição, código, sigla da área e nome do responsável), além de realizar o **Destaque de Etapas** (se o termo bater com a descrição ou o responsável de uma etapa interna, o card da Ação correspondente permanece visível e o painel se expande automaticamente, destacando a etapa com um contorno ciano suave).
  - **Na Home (`home.html`):** Agora o filtro também atua na página inicial, pesquisando e filtrando dinamicamente os cards de **Eixos** e **Áreas** visíveis à medida que o usuário digita.
  - **Abordagem Robusta:** Substituímos seletores de CSS de classes de utilidade utilitárias por buscas via `textContent`, tornando o mecanismo de pesquisa totalmente imune a futuras alterações visuais de classes de cores ou espaçamentos.
- Se o campo de pesquisa for limpo, todos os elementos retornam ao estado original de exibição.

### 5. Limpeza de Interface
- Removemos por completo o botão "Ajuda / Tira-Dúvidas" (ícone de interrogação) do cabeçalho conforme solicitado pelo usuário.

### 6. Sanitização Automática de Nomes Duplicados
- **Detecção e Remoção de Redundâncias Consecutivas:** Desenvolvemos um algoritmo em [utils.py](file:///Users/mpgo/Documents/Projetos%20P%C3%B3s%20Gradua%C3%A7%C3%A3o/PGI/pgi/utils.py) que identifica e remove subsequências de palavras consecutivas repetidas em um nome. Isso corrige automaticamente o caso real `'THAISE REGINA GOUVEIA DE REGINA GOUVEIA DE MIRANDA'` para `'THAISE REGINA GOUVEIA DE MIRANDA'`, independentemente do tamanho da repetição.
- **Integração Híbrida e Local:** O algoritmo é aplicado de forma transparente através de um *monkey patch* sobre a propriedade `nome` da classe `KeycloakUser` do SDK, bem como sobre a implementação do método `get_full_name()` e `__str__()` no modelo de Usuário customizado do Django em [models.py](file:///Users/mpgo/Documents/Projetos%20P%C3%B3s%20Gradua%C3%A7%C3%A3o/PGI/pgi/models.py).
- **Testes de Unidade:** Adicionamos um conjunto completo de testes de regressão em [tests.py](file:///Users/mpgo/Documents/Projetos%20P%C3%B3s%20Gradua%C3%A7%C3%A3o/PGI/pgi/tests.py) cobrindo repetições de subsequências, repetições de palavras simples, nomes normais sem duplicatas e entradas vazias. Todos os testes estão passando com sucesso.

---

## Verificação e Qualidade do Código

### 1. Integridade do Django
O comando de verificação de integridade do Django foi rodado com sucesso no Docker:
```bash
System check identified no issues (0 silenced).
```
Todas as importações de modelos, views, componentes, scripts JS e o context processor estão perfeitamente ajustados e livres de erros de compilação.

### 2. Execução dos Testes Automatizados
Todos os testes de unidade referentes à sanitização de nomes foram validados com êxito dentro do container:
```bash
Found 4 test(s).
System check identified no issues (0 silenced).
....
----------------------------------------------------------------------
Ran 4 tests in 0.006s

OK
```

### 3. Carga de Dados e Teste Local
Todos os usuários de desenvolvimento foram recriados com suas devidas áreas e perfis mapeados perfeitamente pelo script de carga `python manage.py importar_dados`.

---

## Como Realizar os Testes Práticos no Navegador

### 1. Testar o Filtro de Busca Instantâneo
- Entre em qualquer Eixo (ex: **Direitos**).
- No campo **Pesquisar...** do topo direito, digite o código de uma ação que você está vendo (ex: `AI74`). Apenas essa ação ficará visível em tempo real.
- Digite uma palavra que faça parte de uma **Etapa** interna (mesmo que as etapas estejam ocultas). O card da ação continuará visível, o painel se abrirá sozinho e a etapa correspondente será destacada em ciano!

### 2. Testar o Popover de Notificações
- Logue como administrador local (`admin / admin123`).
- Entre em uma ação sob sua responsabilidade, expanda as etapas e adicione um novo andamento (ex: *"Nova entrega técnica efetuada com sucesso"*).
- Clique no sino no topo direito. A notificação com o seu nome, data e texto do andamento aparecerá imediatamente em destaque no topo da lista.

### 3. Testar a Sidebar de Configurações
- Com o usuário `admin` logado, clique em **Configurações** na sidebar esquerda. Você será direcionado para o painel de usuários.
- Crie ou edite uma conta no Django Admin, mudando seu perfil para `Editor` e selecionando a área `SUPLAN`.
- Logue com essa conta de teste (senha local padrão: `mpgo123`).
- Clique em **Configurações** na sidebar esquerda. O modal flutuante aparecerá exibindo suas credenciais: perfil de **Editor** e lotação na área **SUPLAN**.
