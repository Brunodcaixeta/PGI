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

# Entrypoint: prepara o ambiente (banco, migrações, import opcional)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Comando padrão: servidor de desenvolvimento Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
