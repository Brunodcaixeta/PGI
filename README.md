# MPGO Institutional Management Plan (PGI)

![Django](https://img.shields.io/badge/Django-5.0.14-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4.3-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Leia em Português: [README.pt-BR.md](README.pt-BR.md)

## About the Project
The **Institutional Management Plan (PGI)** is a comprehensive web application developed for the MPGO (Ministério Público do Estado de Goiás) to track, manage, and visualize the execution of strategic institutional goals for the 2025–2027 cycle. The system provides an interactive dashboard broken down into strategic axes and functional areas, allowing responsible parties to track and update the evolution of specific actions and their respective stages.

## Key Features
- **Global Dashboard**: Track the overall progress of the institution against the 2025-2027 goal.
- **Axes & Areas Views**: Toggle between strategic axes (e.g., Rights, Institutional Strengthening) and functional areas.
- **Action Tracking**: Detailed views for every institutional action with color-coded progress bars and completion percentages.
- **Granular Stages**: Expandable lists of execution stages with assigned owners and visual completion statuses.
- **Dark Mode First UI**: A modern, glassmorphism-inspired interface using Inter typography and Material Symbols.

## Tech Stack
- **Backend**: Django 5.0.14 (Python)
- **Database**: PostgreSQL 15 (Dockerized)
- **Frontend**: Django Templates + Tailwind CSS v4 (Standalone CLI)
- **Infrastructure**: Docker & Docker Compose

## Quick Start

### 1. Requirements
- Docker and Docker Compose installed on your machine.
- macOS, Linux, or Windows (Tailwind CLI is provided for macOS x64 by default, you may need to download your OS specific binary).

### 2. Run the Database and Server
```bash
# Start PostgreSQL and Django development server
docker compose up -d

# The app will be available at http://localhost:8000/
```

### 3. Compile Tailwind CSS (Development)
The project uses the Tailwind v4 Standalone CLI, avoiding the need for a Node.js environment.
```bash
# Run the compiler in watch mode
./tailwindcss -i pgi/static/pgi/css/input.css -o pgi/static/pgi/css/output.css --watch
```

## Documentation
For detailed technical analysis, architectural decisions, and current implementation plans, please refer to:
- [Technical Analysis (pt-BR)](analise.md)
- [Implementation Plan (pt-BR)](plano.md)

## License
Confidential and proprietary application for internal MPGO use.
