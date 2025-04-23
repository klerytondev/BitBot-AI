from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

retriever = Chroma(persist_directory="db/chroma", embedding_function=OpenAIEmbeddings()).as_retriever()
qa = RetrievalQA.from_chain_type(llm=None, retriever=retriever, chain_type="stuff")

pergunta = input("Pergunte algo: ")
resposta = qa.run(pergunta)
print(resposta)
