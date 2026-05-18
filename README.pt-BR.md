# Plano de Gestão Institucional (PGI) - MPGO

![Django](https://img.shields.io/badge/Django-5.0.14-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4.3-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Read in English: [README.md](README.md)

## Sobre o Projeto
O **Plano de Gestão Institucional (PGI)** é uma aplicação web completa desenvolvida para o Ministério Público do Estado de Goiás (MPGO) com o objetivo de acompanhar, gerenciar e visualizar a execução das metas estratégicas da instituição para o ciclo 2025–2027. O sistema oferece um dashboard interativo dividido por eixos estratégicos e áreas de atuação, permitindo que os responsáveis atualizem e acompanhem a evolução de ações específicas e suas respectivas etapas.

## Principais Funcionalidades
- **Dashboard Global**: Acompanhe o progresso geral da instituição em relação à meta do triênio 2025-2027.
- **Visão por Eixos e Áreas**: Alterne a visualização entre os eixos estratégicos (ex: Direitos, Fortalecimento Institucional) e as áreas funcionais.
- **Acompanhamento de Ações**: Visualização detalhada de cada ação institucional com barras de progresso coloridas e percentuais de conclusão.
- **Etapas Granulares**: Listas expansíveis de etapas de execução com status visuais de conclusão e responsáveis vinculados.
- **Interface Dark Mode First**: Um design moderno focado em glassmorphism, utilizando tipografia Inter e ícones Material Symbols.

## Stack Tecnológica
- **Backend**: Django 5.0.14 (Python)
- **Banco de Dados**: PostgreSQL 15 (via Docker)
- **Frontend**: Django Templates + Tailwind CSS v4 (CLI Standalone)
- **Infraestrutura**: Docker & Docker Compose

## Instalação e Uso Rápido

### 1. Pré-requisitos
- Docker e Docker Compose instalados.
- O executável do Tailwind CLI foi baixado para macOS x64. Se utilizar Windows ou Linux (ou mac ARM), será necessário baixar a versão compatível com sua arquitetura.

### 2. Rodando o Banco de Dados e o Servidor
```bash
# Inicia o PostgreSQL e o servidor de desenvolvimento do Django
docker compose up -d

# A aplicação estará disponível em http://localhost:8000/
```

### 3. Compilando o Tailwind CSS (Modo Desenvolvimento)
O projeto usa o CLI standalone do Tailwind v4, o que dispensa a necessidade de um ambiente Node.js.
```bash
# Executa o compilador observando as alterações em tempo real
./tailwindcss -i pgi/static/pgi/css/input.css -o pgi/static/pgi/css/output.css --watch
```

## Documentação Técnica
Para análises técnicas mais aprofundadas, arquitetura do sistema e próximos passos, consulte:
- [Análise Técnica (analise.md)](analise.md)
- [Plano de Implementação (plano.md)](plano.md)

## Licença
Aplicação confidencial de propriedade do MPGO para uso interno.
