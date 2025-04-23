from langgraph.graph import StateGraph, END
from langchain.agents import tool
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

@tool
def buscar_na_api(consulta: str) -> str:
    return f"[API] Resultado para: {consulta}"

@tool
def buscar_no_vector(consulta: str) -> str:
    return f"[VectorDB] Resposta baseada nos embeddings para: {consulta}"

# LLM base
llm = OpenAI()

# Prompt de decisão
prompt = PromptTemplate.from_template("""
Dada a pergunta: {input}, decida se a resposta deve vir da API ou do VectorDB.
Responda apenas com "api" ou "vector".
""")

decision_chain = LLMChain(llm=llm, prompt=prompt)

# Estados do LangGraph
nodes = {
    "decidir": lambda state: {"rota": decision_chain.run(state["input"]).strip()},
    "api": lambda state: {"resposta": buscar_na_api.run(state["input"]), "fim": True},
    "vector": lambda state: {"resposta": buscar_no_vector.run(state["input"]), "fim": True},
}

builder = StateGraph()
builder.add_node("decidir", nodes["decidir"])
builder.add_node("api", nodes["api"])
builder.add_node("vector", nodes["vector"])

builder.set_entry_point("decidir")
builder.add_conditional_edges("decidir", lambda x: x["rota"], {"api": "api", "vector": "vector"})
builder.add_edge("api", END)
builder.add_edge("vector", END)

graph = builder.compile()

def executar_agente(pergunta):
    resultado = graph.invoke({"input": pergunta})
    return resultado.get("resposta")