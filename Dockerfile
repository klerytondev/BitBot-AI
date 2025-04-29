FROM python:3.10

WORKDIR /app

# Instala dependências do sistema operacional
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências e instala os pacotes Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Cria o diretório para o banco de dados
RUN mkdir -p db/

# Copia o restante do código para o container
COPY . .

# Comando para iniciar o Streamlit apontando para o arquivo correto
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]