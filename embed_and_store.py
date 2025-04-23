from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
import os

os.environ["OPENAI_API_KEY"] = "sua-chave-openai"

def inserir_embeds():
    docs = ["Bitcoin e um ativo digital descentralizado."]
    db = Chroma(persist_directory="db/chroma", embedding_function=OpenAIEmbeddings())
    db.add_texts(docs)