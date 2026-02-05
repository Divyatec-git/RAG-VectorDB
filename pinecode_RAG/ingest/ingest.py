from .loader import load_documents
from .cleaner import clean_text
from .chunker import chunk_text
from app.embeddings import embed_text
from app.vectordb import index


def ingest(folder="data/docs"):

    try:

        docs = load_documents(folder)

        all_chunks = []
        all_metadata = []
        all_ids = []

        idx = 0

        # 1. Clean + chunk documents
        for doc in docs:
            cleaned_text = clean_text(doc["text"])
            chunks = chunk_text(cleaned_text)
          
            for chunk in chunks:
                all_chunks.append(chunk)
                all_metadata.append({
                    "text": chunk,
                    "source": doc['source'],
                    "page": (doc['page'] + 1) if doc['page'] is not None else 1
                })
                all_ids.append(f"chunk_{idx}")
                idx += 1

        # 2. Embed ALL chunks at once (efficient)
        embeddings = embed_text(all_chunks)  # returns List[List[float]]

        # 3. Build Pinecone vectors
        vectors = []
        for i in range(len(all_chunks)):
            vectors.append({
                "id": all_ids[i],
                "values": embeddings[i],
                "metadata": all_metadata[i]
            })

        # 4. Upsert to Pinecone
        index.upsert(vectors=vectors)

        print(f"Ingested {len(all_chunks)} chunks into Pinecone")
    except Exception as e:
        print(e,"error------------------")

if __name__ == "__main__":
    ingest()
