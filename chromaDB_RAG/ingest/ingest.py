from .loader import load_documents
from .cleaner import clean_text
from .chunker import chunk_text
from app.embeddings import embed_text
from app.vectordb import collection

def ingest(folder="data/docs"):
    docs = load_documents(folder)

    all_chunks = []
    metadatas = []
    ids = []

    idx = 0

    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)

        for chunk in chunks:
            all_chunks.append(chunk)
            metadatas.append({
                "source": doc["source"],
                "page": doc["page"]
            })
            ids.append(f"chunk_{idx}")
            idx += 1

    embeddings = embed_text(all_chunks)

    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Ingested {len(all_chunks)} chunks {len(all_chunks[0])}")
if __name__ == "__main__":
    ingest()
