from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import sqlite3
import os
import json

# Verifica e cria o diretório 'db/' se necessário
db_dir = "db/"
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
    print(f"Diretório '{db_dir}' criado com sucesso.")

# Configuração da chave da API OpenAI
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"

# Caminho para o banco SQLite
SQLITE_DB_PATH = "db/crypto_data.sqlite"

# Função para inicializar o banco SQLite
def inicializar_banco_sqlite():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consulta TEXT,
            tipo TEXT,
            resultado TEXT,
            embedding TEXT
        )
    """)
    conn.commit()
    conn.close()

# Função para inserir dados no SQLite e no Chroma
def inserir_embeds(dados: dict):
    """
    Insere os dados retornados pelas tools no SQLite e no Chroma VectorDB.

    Args:
        dados (dict): Dicionário contendo os campos 'consulta', 'tipo', 'resultado'.
    """
    # Inicializa o banco SQLite, se necessário
    inicializar_banco_sqlite()

    # Converte o resultado para JSON (caso seja um dicionário)
    resultado_json = json.dumps(dados.get("resultado", {}))

    # Gera o embedding do texto completo
    texto_para_embedding = f"{dados.get('consulta', '')} {resultado_json}"
    embeddings = OpenAIEmbeddings()
    embedding_vector = embeddings.embed_query(texto_para_embedding)

    # Salva no SQLite
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO crypto_data (consulta, tipo, resultado, embedding)
        VALUES (?, ?, ?, ?)
    """, (dados.get("consulta", ""), dados.get("tipo", ""), resultado_json, json.dumps(embedding_vector)))
    conn.commit()
    conn.close()

    # Salva no Chroma VectorDB
    db = Chroma(persist_directory="db/chroma", embedding_function=embeddings)
    db.add_texts([texto_para_embedding], metadatas=[dados], ids=[str(cursor.lastrowid)])