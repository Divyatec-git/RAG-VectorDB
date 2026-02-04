import os
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

client = genai.Client(api_key=api_key)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Load and Chunk Data
def load_data(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    # Simple chunking by line for this demo
    chunks = [line.strip() for line in text.split('\n') if line.strip()]
    return chunks

chunks = load_data("data.txt")
print(f"Loaded {len(chunks)} chunks.")

# 3. Create Embeddings
print("Generating embeddings...")
embeddings = embedder.encode(chunks)
dimension = embeddings.shape[1]

# 4. Create FAISS Index
print("Creating FAISS index...")
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
print(f"Index contains {index.ntotal} vectors.")

# 5. Search Function
def search(query, k=3):
    query_vector = embedder.encode([query])
    distances, indices = index.search(query_vector, k)
    
    results = []
    for i in range(k):
        idx = indices[0][i]
        results.append(chunks[idx])
    
    return results

# 6. Generate Answer Function
def generate_answer(query, context_chunks):
    context = "\n".join(context_chunks)
    prompt = f"""
    You are a helpful assistant. Use the context below to answer the question.
    
    Context:
    {context}
    
    Question: {query}
    
    Answer:
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating answer: {e}"

# 7. Main Loop
if __name__ == "__main__":
    print("\n--- Simple FAISS RAG ---")
    print("Ask a question about FAISS, RAG, or Gemini (or Type 'exit' to quit).")
    
    while True:
        query = input("\nQuestion: ")
        if query.lower() in ['exit', 'quit']:
            break
            
        print("Searching...")
        context_chunks = search(query)
        print(f"Found {len(context_chunks)} relevant chunks.")
        
        print("Generating answer...")
        answer = generate_answer(query, context_chunks)
        
        print(f"\nAnswer: {answer}")
