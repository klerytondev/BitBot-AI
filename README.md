# GenAI Agent com API pública, RAG e VectorDB

## 💡 Visão Geral
Este projeto implementa um agente inteligente que utiliza dados da API CoinGecko, gera embeddings, armazena informações no SQLite e ChromaDB, e responde perguntas usando RAG (Retrieval-Augmented Generation) ou dados em tempo real, conforme decisão da IA.

## 🚀 Como Rodar
Certifique-se de ter o Docker instalado. Para iniciar o projeto, execute o seguinte comando:

```bash
docker-compose up --build
```

## � Dependências Principais
- **LangChain**: Framework para construção de agentes baseados em LLMs.
- **LangGraph**: Gerenciamento de fluxos de decisão para agentes.
- **ChromaDB**: Banco de dados vetorial para armazenamento e recuperação de embeddings.
- **SQLite**: Banco de dados relacional para persistência de dados estruturados.
- **Streamlit**: Interface web para interação com o agente.
- **OpenAI API**: Geração de embeddings e respostas baseadas em LLMs.
- **Requests**: Para chamadas HTTP à API CoinGecko.

## �📈 Métricas
- **Armazenamento**: ChromaDB local e SQLite.
- **Custo estimado por 1000 tokens (OpenAI)**: ~\$0.0004.
- **Tempo médio de resposta**: ~2 segundos.

## 🧪 Exemplos de Uso
- **Pergunta**: "Qual o preço atual do Bitcoin?"
  - Resposta: Usa a API pública da CoinGecko para obter o preço em tempo real.
- **Pergunta**: "O que é o Bitcoin?"
  - Resposta: Recupera informações semânticas do banco vetorial (RAG).
- **Pergunta**: "Qual foi a variação do Ethereum nos últimos 12 meses?"
  - Resposta: Calcula a variação percentual com base no histórico de preços da CoinGecko.

## 🛠️ Tecnologias
- **LangChain**: Para integração com LLMs e ferramentas.
- **LangGraph**: Para gerenciar fluxos de decisão baseados em estados.
- **ChromaDB**: Banco de dados vetorial para recuperação de informações.
- **SQLite**: Banco de dados relacional para persistência de dados estruturados.
- **Streamlit**: Interface web para interação com o agente.
- **Docker**: Para containerização e fácil implantação.

## 📜 Estrutura do Projeto
- **`agent.py`**: Contém a lógica principal do agente, incluindo o fluxo de decisão e integração com ferramentas.
- **`app.py`**: Interface web construída com Streamlit para interação com o agente.
- **`coingecko_loader.py`**: Funções para buscar dados da API CoinGecko, como preços atuais e históricos.
- **`embed_and_store.py`**: Geração de embeddings e armazenamento no SQLite e ChromaDB.
- **`README.md`**: Documentação do projeto.

## 🧩 Funcionalidades
1. **Busca em API Pública**:
   - Obtém preços atuais e históricos de criptomoedas usando a API CoinGecko.
2. **Armazenamento Vetorial**:
   - Gera embeddings com OpenAI e armazena no ChromaDB para recuperação semântica.
3. **Decisão Inteligente**:
   - Decide automaticamente entre usar a API ou o banco vetorial com base na pergunta do usuário.
4. **Interface Web**:
   - Permite interação com o agente via Streamlit, exibindo histórico de perguntas e respostas.

## 🛠️ Como Contribuir
1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b minha-feature`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`).
4. Envie para a branch principal (`git push origin minha-feature`).
5. Abra um Pull Request.

## 📝 Licença
Este projeto está licenciado sob a [MIT License](LICENSE).