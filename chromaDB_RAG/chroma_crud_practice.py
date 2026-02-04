import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import hashlib

# ---- Embedding model (FREE)
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(texts):
    return model.encode(texts).tolist()

def load_text(path):
    with open(path, "r") as f:
        return f.read()



# ---- Chroma client (persistent)
client = chromadb.PersistentClient(path="./chromaCrud")


collection = client.get_or_create_collection("practice")

def create_document(text, source):
    doc_id = hashlib.md5(text.encode()).hexdigest()

    collection.add(
        documents=[text],
        embeddings=embed([text]),
        metadatas=[{"source": source}],
        ids=[doc_id]
    )

    print("✅ Document added with ID:", doc_id)
    return doc_id

def read_document(doc_id):
    result = collection.get(
        ids=[doc_id],
        include=["documents", "metadatas"]
    )
    print("📖 Retrieved document:")
    print(result)

def update_document(doc_id, new_text):
    collection.update(
        ids=[doc_id],
        documents=[new_text],
        embeddings=embed([new_text]),
        metadatas=[{"source": "sample.txt", "updated": True}]
    )

    print("✏️ Document updated")

def query_document(question):
    results = collection.query(
        query_embeddings=embed([question]),
        n_results=1
    )

    print("🔍 Query result:",results['distances'])
    print(results["documents"][0][0])

def delete_document(doc_id):
    collection.delete(ids=[doc_id])
    print("🗑️ Document deleted")

def get_doc_ids_by_source(source):
    result = collection.get(
        where={"source": source},
        
    )
 
    return result["ids"]

if __name__ == "__main__":
    text = load_text("data/docs/sample.txt")

    # CREATE
    # doc_id = create_document(text, "sample.txt")

    # READ
    # read_document(doc_id)

    # UPDATE
    ids = get_doc_ids_by_source("sample.txt")
  


    if not ids:
        print("❌ Document ID not found. Update aborted.")
        

    # updated_text = text + "\nphp is often used together with this."
    # update_document(ids[0], updated_text)

    # QUERY
    query_document("What is php used for?")

    # DELETE
    # delete_document(ids[0])

    # VERIFY DELETE
    print("📊 Total documents in collection:", collection.count())
