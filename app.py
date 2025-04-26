import streamlit as st
from agent import executar_agente

st.set_page_config(page_title="GenAI Agent com LangGraph", page_icon="🧠")
st.title("🧠 GenAI Agent com API + RAG")

st.markdown("""
Este aplicativo usa um agente baseado em LangGraph para decidir entre:
- Buscar dados reais via API pública (CoinGecko)
- Recuperar contexto semântico via RAG (ChromaDB)
""")

# Inicializa o histórico como uma variável de sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

pergunta = st.text_input("Digite sua pergunta:")
if pergunta:
    with st.spinner("Consultando agente..."):
        resposta = executar_agente(pergunta)
        # Adiciona a interação ao histórico
        st.session_state.historico.append({"pergunta": pergunta, "resposta": resposta})
    
    st.success("Resposta:")
    st.write(resposta)

    # Exibe o histórico completo
    st.markdown("### Histórico de Interações")
    for interacao in st.session_state.historico:
        st.markdown(f"**Usuário:** {interacao['pergunta']}")
        st.markdown(f"**IA:** {interacao['resposta']}")