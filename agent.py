from langgraph.graph import StateGraph, END
from langchain.agents import tool

@tool
def buscar_na_api(consulta: str) -> str:
    # Simulação de busca na API pública
    return f"[API] Resultado para: {consulta}"

@tool
def buscar_no_vector(consulta: str) -> str:
    # Simulação de busca no vectorDB
    return f"[VectorDB] Resposta baseada nos embeddings para: {consulta}"

tools = [buscar_na_api, buscar_no_vector]

# TODO: Montar grafo com LangGraph e estados personalizados