# RAG Chatbot Project Documentation

This document explains how the RAG (Retrieval-Augmented Generation) chatbot project works, detailing every file, the data flow, and the core concepts like embeddings and vector databases. It is written for beginners to understand the entire system.

## 1. How the Project Works (High-Level Overview)

This project is a **RAG (Retrieval-Augmented Generation) Chatbot**. It allows users to ask questions about specific documents (like PDFs or text files), and the AI answers based *only* on the information in those documents.

It works in two main phases:

### Phase 1: Ingestion (Preparing the Data)
1.  **Load**: We read PDF or text files from the `data/` folder.
2.  **Clean**: We fix broken text (like weird spaces or newlines) so the AI can read it better.
3.  **Chunk**: We split large documents into smaller pieces ("chunks") because AI models have a limit on how much text they can read at once.
4.  **Embed**: We convert these text chunks into lists of numbers called **Vectors** or **Embeddings**.
5.  **Store**: We save these vectors in a **Vector Database** (ChromaDB) so we can search them later.

### Phase 2: Retrieval & Answering (The Chat)
1.  **Ask**: The user sends a question to the API.
2.  **Search**: We convert the user's question into numbers (embedding) and find the most similar document chunks in our database.
3.  **Generate**: We send the user's question + the found relevant text (context) to an AI model (like Google Gemini).
4.  **Answer**: The AI uses the context to answer the question accurately.

---

## 2. File Structure & Responsibilities

Here is how each file helps the project:

### `ingest/` Directory (Data Preparation)
*   **`loader.py`**:
    *   **Role**: The "Reader".
    *   **Details**: It looks into the `data/` folder. If it finds a PDF, it uses `pypdf` to extract text page by page. If it finds a `.txt` file, it just reads it. It records which file and page the text came from (metadata).
*   **`cleaner.py`**:
    *   **Role**: The "Janitor".
    *   **Details**: Raw text from PDFs is often messy (e.g., words split across lines). This file removes extra spaces, fixes broken newlines, and deletes weird characters (null bytes) to make the text "clean" for the AI.
*   **`chunker.py`**:
    *   **Role**: The "Scissors".
    *   **Details**: It takes the long clean text and cuts it into smaller pieces (chunks), usually around 800 "tokens" (roughly words). It uses an "overlap" (e.g., 100 tokens) so that sentences aren't cut in the middle of a thought.
*   **`ingest.py`**:
    *   **Role**: The "Manager".
    *   **Details**: This script runs the whole show. It calls `loader` -> `cleaner` -> `chunker`, then generates embeddings, and finally saves everything into the database. You run this file *once* whenever you add new documents.

### `app/` Directory (The Application)
*   **`embeddings.py`**:
    *   **Role**: The "Translator".
    *   **Details**: It uses a model called `all-MiniLM-L6-v2` to turn text into numbers (vectors). This is crucial for comparing meanings.
*   **`vectordb.py`**:
    *   **Role**: The "Librarian" (Database).
    *   **Details**: It manages `ChromaDB`. It sets up a persistent folder (`./chroma`) so your data is saved on your hard drive. It allows saving and searching for vectors.
*   **`rag.py`**:
    *   **Role**: The "Brain".
    *   **Details**: This contains the core logic:
        1.  `retrieve(query)`: Finds relevant chunks from DB.
        2.  `build_prompt(...)`: Combines the question and the found chunks into instructions for the AI.
        3.  `call_llm(...)`: Sends the prompt to Google Gemini API and gets the final answer.
*   **`main.py`**:
    *   **Role**: The "Door" (API).
    *   **Details**: It uses **FastAPI** to create a web server. It defines an endpoint `/chat` where the frontend or user sends a JSON message (`{"query": "..."}`), and it returns the answer.

---

## 3. Deep Dive Topics

### How Data Cleaning Works (`cleaner.py`)
Data cleaning is simple but essential. The code does three main things:
1.  **Replace Newlines**: `text.replace("\n", " ")`. PDFs often put newlines in the middle of sentences. We replace them with spaces to make one flowing paragraph.
2.  **Remove Multiple Spaces**: `re.sub(r"\s+", " ", text)`. If there are 5 spaces in a row, this turns them into 1 space.
3.  **Remove Null Bytes**: These are invisible characters that can crash some database or AI systems.

**Why?** If the text is messy, the AI might misunderstand the sentence structure, leading to bad answers.

---

### Embeddings: Creation & Purpose

#### What are they?
Embeddings are lists of numbers (vectors) that represent the *meaning* of text.
*   "Dog" -> `[0.1, 0.5, -0.2]`
*   "Puppy" -> `[0.1, 0.55, -0.1]` (Very close numbers!)
*   "Car" -> `[0.9, -0.8, 0.3]` (Very different numbers)

#### How are they created? (`ingest.py` & `app/embeddings.py`)
We use a library called `sentence_transformers`.
1.  We give the model our text chunk: `"The sky is blue."`
2.  The model runs complex math and outputs a list of 384 numbers.
3.  We typically generate embeddings for *chunks* of text, not single words.

#### Why do we need them?
Computers can't "read" English. They only understand math. By converting text to numbers, we can calculate the **distance** between two pieces of text.
*   If the user asks "How to reset password?", we compare the numbers of that question against the numbers of all our document chunks. The chunks with the "closest" numbers are the ones talking about passwords.

---

### ChromaDB: How it Works

**ChromaDB** is the Vector Database used in this project.

#### Storage
*   In `vectordb.py`, we initialize it with `PersistentClient(path="./chroma")`.
*   This means it saves all the data into a folder named `chroma/` on your computer. If you restart the app, the data is still there.

#### Organization
*   Data is stored in a **Collection** (named `"rag_docs"`). Think of a Collection like a "Table" in SQL or a "Sheet" in Excel.

#### Searching
*   When we query ChromaDB:
    1.  We give it the vector of the user's question.
    2.  It uses an algorithm (like **HNSW**) to quickly find the "Nearest Neighbors" (closest vectors) in the database.
    3.  It returns the stored text chunk associated with those vectors.

#### Why ChromaDB?
*   It handles the complexity of vector math for us.
*   It is fast (can search thousands of documents in milliseconds).
*   It runs locally (no need to pay for a cloud database).
