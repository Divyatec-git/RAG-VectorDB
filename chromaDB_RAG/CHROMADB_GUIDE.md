# Deep Dive: How ChromaDB Works

This guide explains the inner workings of ChromaDB, the vector database used in this project. It covers the core concepts, the data structure, and detailed explanations of the main methods: `create`, `add`, `update`, `get`, and `query`.

## 1. Visual Overview

Here is how data flows into and out of ChromaDB:

```mermaid
graph TD
    User([User / Code])
    
    subgraph "ChromaDB Client"
        Collection[Collection]
    end
    
    subgraph "Storage (./chroma)"
        VectorIndex[Vector Index (HNSW)]
        MetadataStore[Metadata Store (SQLite)]
    end
    
    User -- "1. Add(Text, Embeddings)" --> Collection
    Collection -- "Save Vectors" --> VectorIndex
    Collection -- "Save Text & Metadata" --> MetadataStore
    
    User -- "2. Query(Question Vector)" --> Collection
    Collection -- "Nearest Neighbor Search" --> VectorIndex
    VectorIndex -- "Return IDs" --> Collection
    Collection -- "Fetch Text by IDs" --> MetadataStore
    MetadataStore -- "Return Documents" --> User
```

---

## 2. Core Concepts

*   **Client**: The main entry point. It manages the connection to the database (either in-memory or saved to disk).
*   **Collection**: Think of this like a *table* in SQL or a *folder* of files. It groups related documents together.
*   **Document**: The actual text content.
*   **Embedding**: The list of numbers representing the meaning of the document.
*   **Metadata**: Extra info about the document (e.g., `{"source": "manual.pdf", "page": 10}`).
*   **ID**: A unique name for each chunk (e.g., `"chunk_1"`).

---

## 3. Detailed Methods

### Initialization (`get_or_create_collection`)

Before doing anything, you need a collection.

```python
import chromadb

# 1. Start the client (saves to disk)
client = chromadb.PersistentClient(path="./chroma")

# 2. Get or Create a collection
collection = client.get_or_create_collection(name="rag_docs")
```

---

### A. ADD (Inserting Data)

Use `.add()` to insert new data.
*   **Requirement**: IDs must be unique. If you try to add an ID that exists, it will error.
*   **Automatic Embedding**: If you don't provide `embeddings`, Chroma will use a default model to generate them (unless configured otherwise). In our project, we generate them ourselves first.

```python
collection.add(
    documents=["This is a document about cats.", "This is about dogs."],
    metadatas=[{"category": "animal"}, {"category": "animal"}],
    ids=["id1", "id2"],
    embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]] # Optional if using built-in embedding function
)
```

---

### B. GET (Fetching Data)

Use `.get()` to retrieve data by ID or filter by metadata. This is **NOT** a semantic search; it's a direct lookup (like `SELECT * FROM table WHERE ...`).

```python
# Get specific documents by ID
results = collection.get(ids=["id1"])

# Get all documents where metadata source is "manual.pdf"
results = collection.get(
    where={"source": "manual.pdf"}
)
```

**Output format:**
```json
{
  "ids": ["id1"],
  "embeddings": None,
  "metadatas": [{"source": "manual.pdf", "page": 1}],
  "documents": ["Text content..."]
}
```

---

### C. QUERY (Semantic Search)

Use `.query()` to find the *most similar* documents to a question. This is the heart of RAG.

```python
results = collection.query(
    query_embeddings=[[0.1, 0.2, ...]], # Vector of the question
    n_results=2,                        # How many matches to return
    where={"category": "animal"}        # Optional: Filter before searching
)
```
*   **How it works**: It calculates the "distance" between the query vector and all stored vectors. Smaller distance = more similar.

---

### D. UPDATE (Modifying Data)

Use `.update()` to change existing data.
*   **Requirement**: The ID *must* exist. If it doesn't, it will error.

```python
collection.update(
    ids=["id1"],
    documents=["This is the NEW text for id1."],
    metadatas=[{"category": "mammal"}]
)
```
*   *Note*: If you update the document text, you usually need to update the embedding too!

---

### E. UPSERT (Update or Insert)

Use `.upsert()` if you aren't sure if the ID exists.
*   If ID exists -> Updates it.
*   If ID doesn't exist -> Adds it.

```python
collection.upsert(
    ids=["id1"],
    documents=["This is text."],
    metadatas=[{"category": "test"}]
)
```
*   **Best Practice**: Use this when re-running ingestion scripts to avoid "ID already exists" errors.

---

### F. DELETE (Removing Data)

Use `.delete()` to remove items.

```python
# Delete by ID
collection.delete(ids=["id1"])

# Delete all chunks from a specific file
collection.delete(
    where={"source": "old_manual.pdf"}
)
```

---

## 4. Cheat Sheet

| Method | Purpose | Use Case |
| :--- | :--- | :--- |
| **`add`** | Insert new data | Initial loading of documents. |
| **`get`** | Fetch by ID/Metadata | Checking what's in the DB, debugging. |
| **`query`** | Search by meaning | The chatbot asking "What matches this question?". |
| **`update`** | Modify existing | Fixing a typo in a document. |
| **`upsert`** | Smart Add/Update | Re-running ingestion without errors. |
| **`delete`** | Remove data | Removing outdated documents. |
