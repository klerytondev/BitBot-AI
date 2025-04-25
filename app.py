import streamlit as st
from agent import executar_agente

st.set_page_config(page_title="GenAI Agent com LangGraph", page_icon="🧠")
st.title("🧠 GenAI Agent com API + RAG")

st.markdown("""
Este aplicativo usa um agente baseado em LangGraph para decidir entre:
- Buscar dados reais via API pública (CoinGecko)
- Recuperar contexto semântico via RAG (ChromaDB)
""")

pergunta = st.text_input("Digite sua pergunta:")
if pergunta:
    with st.spinner("Consultando agente..."):
        resposta = executar_agente(pergunta)
    st.success("Resposta:")
    st.write(resposta)