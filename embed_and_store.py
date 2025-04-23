from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os

os.environ["OPENAI_API_KEY"] = "sua-chave-openai"

def inserir_embeds():
    db = Chroma(persist_directory="db/chroma", embedding_function=OpenAIEmbeddings())
    db.add_texts([texto])