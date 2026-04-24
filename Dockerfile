# Usar Python 3.12 (leve)
FROM python:3.12-slim

# Variáveis de ambiente importantes para o Python (não gerar arquivos .pyc e logs em tempo real)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar o restante do código do projeto para o container
COPY . /app/
