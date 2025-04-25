from langgraph.graph import StateGraph, END
from langchain.agents import tool
from langchain.llms import OpenAI
from datetime import datetime
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from coingecko_loader import buscar_cripto_info
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import requests
import os
from embed_and_store import inserir_embeds

@tool
def buscar_na_api(consulta: str) -> str:
    resposta = buscar_cripto_info(consulta)
    if resposta:
        inserir_embeds(resposta)  # Salva a resposta no banco vetorizado
    return resposta

@tool
def buscar_historico_preco(cripto: str) -> str:
    """Busca a variação de preço de uma cripto nos últimos 12 meses."""
    url = f"https://api.coingecko.com/api/v3/coins/{cripto}/market_chart?vs_currency=usd&days=365"
    r = requests.get(url)
    if r.status_code != 200:
        return f"Erro ao buscar dados de {cripto}: {r.text}"
    
    data = r.json()
    prices = data["prices"]  # Lista de [timestamp, preço]
    
    preco_inicial = prices[0][1]
    preco_final = prices[-1][1]
    variacao = ((preco_final - preco_inicial) / preco_inicial) * 100

    data_inicial = datetime.fromtimestamp(prices[0][0] / 1000).strftime("%d/%m/%Y")
    data_final = datetime.fromtimestamp(prices[-1][0] / 1000).strftime("%d/%m/%Y")

    resposta = (
        f"De {data_inicial} até {data_final}, o preço do {cripto} variou "
        f"de ${preco_inicial:.2f} para ${preco_final:.2f}, uma mudança de {variacao:.2f}%."
    )

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
- "historico" (caso fale sobre desempenho ao longo do tempo),
- "api" (para preço atual),
- "vector" (para perguntas explicativas, como "o que é Bitcoin").

Responda apenas com: historico, api ou vector.
""")

decision_chain = LLMChain(llm=llm, prompt=prompt)

# Estados do LangGraph
nodes = {
    "decidir": lambda state: {"input": state["input"], "rota": decision_chain.run(state["input"]).strip()},
    "api": lambda state: {"resposta": buscar_na_api.run(state["input"]), "fim": True},
    "vector": lambda state: {"resposta": buscar_no_vector.run(state["input"]), "fim": True},
    "historico": lambda state: {
        "resposta": buscar_historico_preco.run(state["input"]), "fim": True
    },
}

builder = StateGraph()
builder.add_node("decidir", nodes["decidir"])
builder.add_node("api", nodes["api"])
builder.add_node("vector", nodes["vector"])
builder.add_node("historico", nodes["historico"])  # novo nó

builder.set_entry_point("decidir")
builder.add_conditional_edges("decidir", lambda x: x["rota"], {
    "api": "api",
    "vector": "vector",
    "historico": "historico"
})
builder.add_edge("api", END)
builder.add_edge("vector", END)
builder.add_edge("historico", END)

graph = builder.compile()

def executar_agente(pergunta):
    # Executa o LangGraph para determinar e executar os nós necessários
    resultado = graph.invoke({"input": pergunta})
    
    # Consulta o banco vetorizado com a pergunta original
    db = Chroma(persist_directory="db/chroma", embedding_function=OpenAIEmbeddings())
    retriever = db.as_retriever()
    docs = retriever.get_relevant_documents(pergunta)
    
    # Retorna a resposta do banco vetorizado ou uma mensagem padrão
    return docs[0].page_content if docs else "Sem resposta encontrada no banco vetorial."