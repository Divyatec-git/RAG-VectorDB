# LangChain & Code Guide

This document provides a technical breakdown of the functions and LangChain components used in this project.

## 1. app/rag.py

This file contains the core logic for the Retrieval-Augmented Generation (RAG) pipeline.

### Imports

| Import | Purpose |
| :--- | :--- |
| `HuggingFaceEmbeddings` | **Encoder**: Converts text into vector embeddings using a HuggingFace model. We use it to run the embedding model locally (free). |
| `Chroma` | **Vector Database**: A local vector store that saves our embeddings. It allows us to perform "semantic search" to find relevant documents. |
| `ChatOpenAI` | **LLM Interface**: The LangChain wrapper for OpenAI's Chat API (e.g., GPT-3.5/4). It sends our prompt and context to OpenAI. |
| `ConversationalRetrievalChain` | **The Manager**: A specific chain designed for chat. It combines (1) fetching relevant docs (Retrieval) and (2) answering questions (Generation) while handling memory. |
| `ConversationBufferMemory` | **Memory**: Stores the history of the conversation so the bot remembers previous Q&A pairs (context). |
| `PromptTemplate` | **Instruction**: Defines exactly how we want to format the input to the LLM (e.g., "Use this context..."). |

### Functions

#### `get_embeddings()`
-   **What it does**: Initializes the embedding model.
-   **Why**: We need a consistent way to turn text into numbers. We use `sentence-transformers/all-MiniLM-L6-v2` because it's fast and effective for English.

#### `get_vectorstore()`
-   **What it does**: Connects to the ChromaDB database stored in the `chroma_db` folder.
-   **Why**: To save and retrieve our document chunks. It uses the embedding function to understand the data.

#### `get_rag_chain()`
-   **What it does**: Assembles the entire RAG pipeline.
    1.  Gets the vectorstore and turns it into a `retriever` (an interface for finding docs).
    2.  Sets up the `ChatOpenAI` LLM.
    3.  Creates `memory` to store chat history.
    4.  defines a strict `PromptTemplate` to stop hallucinations.
    5.  Combines them all into a `ConversationalRetrievalChain`.
-   **Returns**: The executable chain object.

---

## 2. app/data_processing.py

This file handles preparing your data before it goes into the database.

### Imports

| Import | Purpose |
| :--- | :--- |
| `RecursiveCharacterTextSplitter` | **Chunker**: Intelligently splits long text into smaller "chunks". It tries to keep paragraphs and sentences together. |

### Functions

#### `clean_text(text: str)`
-   **What it does**: Removes excessive newlines and extra spaces using Regex (`re`).
-   **Why**: Clean text creates better embeddings. Noise (like 10 empty lines) can confuse the model.

#### `chunk_text(text: str)`
-   **What it does**: Splits the cleaned text into chunks of 1000 characters with a 200-character overlap.
-   **Why**:
    -   **Size**: LLMs have a token limit. We can't feed a whole book at once.
    -   **Overlap**: Keeps context across boundaries so sentences aren't cut in half weirdly.

---

## 3. app/main.py

This is the API server that lets the outside world talk to our Python code.

### Functions

#### `ingest_text(file: UploadFile)`
-   **Route**: `POST /ingest`
-   **Logic**:
    1.  Checks if the file is a PDF or Text file.
    2.  **If PDF**: Uses `pypdf.PdfReader` to extract text page by page.
    3.  **If Text**: Decodes the bytes directly.
    4.  Calls `clean_text` -> `chunk_text`.
    5.  Adds the chunks to ChromaDB via `vectorstore.add_documents`.

#### `chat(request: QueryRequest)`
-   **Route**: `POST /chat`
-   **Logic**:
    1.  Receives a user question (`request.query`).
    2.  Calls `rag_chain.invoke({"question": ...})`.
    3.  The chain automatically searches Chroma, gets context, sends it to OpenAI, and returns the answer.
