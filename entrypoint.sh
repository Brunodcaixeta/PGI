#!/bin/bash
# entrypoint.sh - Script de entrada para o container Docker do PGI
#
# Executa preparações necessárias antes de iniciar o servidor Django:
#   1. Aguarda o banco de dados ficar disponível
#   2. Executa as migrações pendentes
#   3. Opcionalmente importa dados dos CSVs (se IMPORT_DATA=true)
#   4. Executa o comando principal (CORS ou argumento passado)

set -e

# ──────────────────────────────────────────────────────────────
# 1. Aguardar banco de dados ficar disponível
# ──────────────────────────────────────────────────────────────
if [ -n "$SQL_HOST" ]; then
    echo "⏳ Aguardando PostgreSQL em $SQL_HOST:$SQL_PORT ..."
    until python -c "
import socket, sys, os
host = os.environ.get('SQL_HOST')
port = int(os.environ.get('SQL_PORT'))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    s.close()
    sys.exit(0)
except:
    sys.exit(1)
" 2>/dev/null; do
        echo "   PostgreSQL não está pronto ainda... aguardando 1s"
        sleep 1
    done
    echo "✅ PostgreSQL está pronto!"
fi

# ──────────────────────────────────────────────────────────────
# 2. Executar migrações do Django
# ──────────────────────────────────────────────────────────────
echo "🚀 Executando migrate..."
python manage.py migrate --noinput

# ──────────────────────────────────────────────────────────────
# 3. Importar dados dos CSVs (opcional)
# ──────────────────────────────────────────────────────────────
if [ "${IMPORT_DATA,,}" = "true" ]; then
    echo "📥 IMPORT_DATA=true detectado — importando dados dos CSVs..."
    python manage.py importar_dados
fi

# ──────────────────────────────────────────────────────────────
# 4. Executar o comando principal
# ──────────────────────────────────────────────────────────────
exec "$@"
