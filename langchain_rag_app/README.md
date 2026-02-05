# LangChain RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with **LangChain**, **FastAPI**, **ChromaDB**, and **OpenAI**. This application allows you to ingest text and PDF documents and ask questions about them.

## Features

-   **RAG Architecture**: Retrieves relevant context from your documents to answer questions.
-   **Strict Context Mode**: The bot is configured to *only* answer based on the provided documents. If the answer isn't there, it says "I don't know".
-   **Multi-Format Support**: Ingests both `.txt` and `.pdf` files.
-   **Free Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` (runs locally via HuggingFace) to save costs.
-   **Persistent Storage**: Uses ChromaDB to save embeddings so you don't need to re-ingest data after restarting.
-   **Dockerized**: Easy deployment with Docker and Docker Compose.

## Project Structure

```
langchain_rag_app/
├── app/
│   ├── main.py             # FastAPI application and endpoints
│   ├── rag.py              # LangChain RAG logic (Chain, Embeddings, VectorStore)
│   ├── data_processing.py  # Text cleaning and chunking logic
│   └── config.py           # Configuration (API Keys, paths)
├── chroma_db/              # Persistent storage for Vector Database
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Orchestration for running the app
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (API Keys)
```

## Prerequisites

-   **Docker** (Recommended) OR **Python 3.9+**
-   **OpenAI API Key** (for the LLM)

## Setup & Running

### 1. Environment Configuration

1.  Clone/Navigate to the directory.
2.  Copy the example env file:
    ```bash
    cp .env.example .env
    ```
3.  Edit `.env` and add your OpenAI API Key:
    ```ini
    OPENAI_API_KEY=sk-proj-...
    ```

### 2. Running with Docker (Recommended)

```bash
# Build and start
docker-compose up --build

# Or with Docker Compose v2
docker compose up --build
```
The API will be available at [http://localhost:8000](http://localhost:8000).

### 3. Running Locally

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

### Ingesting Data

Upload your documents to the vector database.

**Endpoint**: `POST /ingest`

**Example (cURL)**:
```bash
curl --location 'http://localhost:8000/ingest' \
--form 'file=@"/path/to/your/document.pdf"'
```

### Chatting

Ask questions about your documents.

**Endpoint**: `POST /chat`

**Example (cURL)**:
```bash
curl --location 'http://localhost:8000/chat' \
--header 'Content-Type: application/json' \
--data '{
    "query": "What are the key points in the document?"
}'
```

## How It Works

1.  **Ingestion**: When you upload a file, it is read (using `pypdf` for PDFs), cleaned, and split into small chunks (1000 characters).
2.  **Embedding**: Each chunk is converted into a vector (a list of numbers) using the locally running HuggingFace model. These vectors are stored in **ChromaDB**.
3.  **Retrieval**: When you ask a question, the question is also converted into a vector. We search ChromaDB for the chunks most similar to your question.
4.  **Generation**: The most relevant chunks are sent to **GPT-3.5-turbo** (via OpenAI) along with your question. A strict prompt ensures the AI uses *only* those chunks to generate the answer.
