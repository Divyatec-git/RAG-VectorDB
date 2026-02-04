from app.embeddings import embed_text
from app.vectordb import collection,client
import requests
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()


clientData = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def retrieve(query: str, k=4):
    query_embedding = embed_text([query])[0]
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    return results["documents"][0]

def build_prompt(context_chunks, question):
    context = "\n\n".join(context_chunks)

    return f"""
            You are a helpful assistant.
            Answer ONLY using the context below.
            
            Context:
            {context}

            Question:
            {question}
            """
def call_llm_old(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
def call_llm(prompt: str) -> str:
    try:
        response = clientData.models.generate_content( 
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        
        if not response or not response.text:
            return "No response from Gemini"

        return response.text

    except Exception as e:
        return f"Gemini error: {str(e)}"

def rag_answer(question: str):
    chunks = retrieve(question)
    
    prompt = build_prompt(chunks, question)
   
    return call_llm(prompt)
