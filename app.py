import streamlit as st
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

st.set_page_config(page_title="GenAI RAG Streamlit", page_icon="🔎")
st.title("🔎 GenAI com VectorDB")

st.markdown("""
Este aplicativo consulta uma base vetorial local com embeddings OpenAI usando LangChain RetrievalQA.
""")

# Inicializa o retriever e o QA chain
retriever = Chroma(persist_directory="db/chroma", embedding_function=OpenAIEmbeddings()).as_retriever()
qa = RetrievalQA.from_chain_type(llm=None, retriever=retriever, chain_type="stuff")

# Interface
pergunta = st.text_input("Digite sua pergunta:")
if pergunta:
    with st.spinner("Buscando resposta..."):
        resposta = qa.run(pergunta)
    st.success("Resposta:")
    st.write(resposta)
