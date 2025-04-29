from langgraph.graph import StateGraph, END
from langchain.agents import tool
from langchain.llms import OpenAI
from datetime import datetime
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from coingecko_loader import (
    buscar_cripto_info,
    preco_atual,
    historico_preco_12_meses
)
from langchain_community.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os
from embed_and_store import inserir_embeds

@tool
def buscar_na_api(consulta: str) -> str:
    """Busca informações de preço atual ou histórico de uma criptomoeda usando a API do pacote coingecko_loader."""
    resposta = buscar_cripto_info(consulta)
    if resposta:
        inserir_embeds(resposta)  # Salva a resposta no banco vetorizado
    return resposta

@tool
def buscar_historico_preco(cripto: str) -> str:
    """Busca o histórico de preços de uma criptomoeda nos últimos 12 meses usando a API do pacote coingecko_loader."""
    resposta = historico_preco_12_meses(cripto)
    if resposta:
        inserir_embeds(resposta)  # Salva a resposta no banco vetorizado
    return resposta

@tool
def buscar_preco_atual(cripto: str) -> str:
    """Busca o preço atual de uma criptomoeda usando a API do pacote coingecko_loader."""
    resposta = preco_atual(cripto)
    if resposta:
        inserir_embeds(resposta)  # Salva a resposta no banco vetorizado
    return resposta

@tool
def buscar_no_vector(consulta: str) -> str:
    db = Chroma(persist_directory="db/chroma", embedding_function=OpenAIEmbeddings())
    retriever = db.as_retriever()
    docs = retriever.get_relevant_documents(consulta)
    return docs[0].page_content if docs else "Sem resposta encontrada no banco vetorial."

# LLM base
llm = OpenAI()

# Prompt de decisão
prompt = PromptTemplate.from_template("""
Dada a pergunta: {input}, diga se a resposta deve vir de:
- "historico" (caso fale sobre desempenho ao longo do tempo, como "Qual foi a variação do Bitcoin no último ano?"),
- "api" (para informações gerais ou históricas, como "Qual é o preço atual do Ethereum?"),
- "preco_atual" (para perguntas específicas sobre o preço atual, como "Qual é o preço atual do Bitcoin?"),
- "vector" (para perguntas explicativas, como "O que é Bitcoin?").

Responda apenas com: historico, api, preco_atual ou vector.
""")

decision_chain = LLMChain(llm=llm, prompt=prompt)

# Estados do LangGraph
nodes = {
    "decidir": lambda state: {"input": state["input"], "rota": decision_chain.run(state["input"]).strip()},
    "api": lambda state: {"resposta": buscar_na_api.run(state["input"]), "fim": True},
    "vector": lambda state: {"resposta": buscar_no_vector.run(state["input"]), "fim": True},
    "historico": lambda state: {"resposta": buscar_historico_preco.run(state["input"]), "fim": True},
    "preco_atual": lambda state: {"resposta": buscar_preco_atual.run(state["input"]), "fim": True},  # Novo nó
}

builder = StateGraph()
builder.add_node("decidir", nodes["decidir"])
builder.add_node("api", nodes["api"])
builder.add_node("vector", nodes["vector"])
builder.add_node("historico", nodes["historico"])
builder.add_node("preco_atual", nodes["preco_atual"]) 

builder.set_entry_point("decidir")
builder.add_conditional_edges("decidir", lambda x: x["rota"], {
    "api": "api",
    "vector": "vector",
    "historico": "historico",
    "preco_atual": "preco_atual" 
})
builder.add_edge("api", END)
builder.add_edge("vector", END)
builder.add_edge("historico", END)
builder.add_edge("preco_atual", END) 

graph = builder.compile()


def salvar_historico(pergunta: str, resposta: str):
    """Salva a interação (pergunta e resposta) no banco vetorizado."""
    db = Chroma(persist_directory="db/chroma", embedding_function=OpenAIEmbeddings())
    db.add_texts([f"Pergunta: {pergunta}\nResposta: {resposta}"])

def executar_agente(pergunta):
    # Executa o LangGraph para determinar e executar os nós necessários
    resultado = graph.invoke({"input": pergunta})
    
    # Obtém a resposta gerada
    resposta = resultado.get("resposta", "Sem resposta encontrada.")
    
    # Salva a interação no banco vetorizado
    salvar_historico(pergunta, resposta)
    
    # Consulta o banco vetorizado com a pergunta original
    db = Chroma(persist_directory="db/chroma", embedding_function=OpenAIEmbeddings())
    retriever = db.as_retriever()
    docs = retriever.get_relevant_documents(pergunta)
    
    # Retorna a resposta do banco vetorizado ou uma mensagem padrão
    return docs[0].page_content if docs else "Sem resposta encontrada no banco vetorial."