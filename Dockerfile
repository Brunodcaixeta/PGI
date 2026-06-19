# Usar Python 3.12 (leve)
FROM python:3.12-slim

# Variáveis de ambiente importantes para o Python (não gerar arquivos .pyc e logs em tempo real)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências de sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

RUN git config --global http.sslVerify false

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar o restante do código do projeto para o container
COPY . /app/

# Fazer o download do Tailwind CSS standalone para Linux, gerar o CSS e coletar os estáticos
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64 && \
    chmod +x tailwindcss-linux-x64 && \
    mv tailwindcss-linux-x64 /usr/local/bin/tailwindcss && \
    tailwindcss -i ./pgi/static/pgi/css/input.css -o ./pgi/static/pgi/css/output.css --minify && \
    python manage.py collectstatic --noinput

# Entrypoint: prepara o ambiente (banco, migrações, import opcional)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Iniciar a aplicação usando Gunicorn com parâmetros das variáveis de ambiente (ou defaults)
EXPOSE 8000
CMD ["sh", "-c", "gunicorn --workers ${GUNICORN_WORKERS:-4} --timeout ${GUNICORN_TIMEOUT:-60} --bind 0.0.0.0:8000 setup.wsgi:application"]
