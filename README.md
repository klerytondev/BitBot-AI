"""
# GenAI Agent com API pública, RAG e VectorDB

## 💡 Visão Geral
Agente que consulta dados da CoinGecko, gera embeddings, armazena no SQLite + ChromaDB e responde perguntas via RAG.

## 🚀 Como Rodar
```bash
docker-compose up --build
```

## 📈 Métricas
- Armazenamento: ChromaDB local
- Custo estimado por 1000 tokens (OpenAI): ~\$0.0004
- Tempo médio de resposta: ~2s

## 🧪 Exemplos de uso
- Pergunta: "Qual o preço atual do Bitcoin?"
  - Usa API pública da CoinGecko
- Pergunta: "O que é o Bitcoin?"
  - Usa vectorDB local (RAG)

## 🛠️ Tecnologias
LangChain, LangGraph, Chroma, SQLite, Docker, Streamlit
"""