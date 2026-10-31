# ⚖️ Juris-Maroc

### Moroccan Labor Code · Retrieval-Augmented Generation

Ask questions about Morocco's Labor Code (Loi 65-99) in French. Juris-Maroc retrieves relevant legal text and uses it to ground AI-generated answers.

![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.4.3-005571?logo=elasticsearch&logoColor=white)
![uv](https://img.shields.io/badge/dependencies-uv-6B4FBB)

> **Note:** This project is for research and informational purposes. It is not a substitute for advice from a qualified legal professional.

## ✨ What it does

- **Searches legal text:** Supports semantic vector retrieval and lexical BM25 search.
- **Grounds responses in context:** Sends retrieved Labor Code passages to the language model with instructions to answer from that context.
- **Keeps the pipeline extensible:** Separates retrieval from orchestration so search approaches can be adapted independently.

## 🧩 How it works

| Component | Role |
| --- | --- |
| `RAGBase` | Coordinates retrieval, context construction, prompt creation, and Google GenAI requests. |
| `ElasticVectorRAG` | Retrieves passages through multilingual vector search. |
| `ElasticRAG` | Retrieves passages through Elasticsearch lexical search (BM25). |

### Technology

| Layer | Technology |
| --- | --- |
| Vector and lexical search | Elasticsearch 8.4.3 |
| Embeddings | Sentence Transformers · `paraphrase-multilingual-MiniLM-L12-v2` |
| Language model | Google GenAI |
| Data preparation | PyMuPDF and JSON |
| Python dependencies | `uv` |

## 📁 Project structure

```text
LLM_RAG/
├── docker-compose.yaml       # Local Elasticsearch service
├── pyproject.toml            # Project dependencies
├── labor_code_chunks.json    # Prepared Labor Code passages
├── rag_helper.py             # RAG orchestration
├── ingest.py                 # Load passages and build an index
├── extraction.py             # Document extraction utilities
├── vector_search.ipynb       # Vector-search workflow
├── ElasticRag.ipynb          # Elasticsearch lexical-search workflow
└── rag.ipynb                 # RAG experiments
```

## 🚀 Get started

### Prerequisites

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/)
- [Docker Compose](https://docs.docker.com/compose/)
- A Google AI Studio API key

### 1. Start Elasticsearch

Run these commands from the `LLM_RAG` directory:

```bash
docker compose up -d
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure your API key

Create a `.env` file in `LLM_RAG`:

```dotenv
GEMINI_API_KEY=your_google_ai_studio_key
```

### 4. Run a workflow

Open `vector_search.ipynb` or `ElasticRag.ipynb` and run the notebook cells to ingest and query the Labor Code. For example:

```python
user_query = "Quelles sont les conditions de la démission et la rupture de contrat ?"
final_answer = vector_rag_system.rag(user_query)
print(final_answer)
```
