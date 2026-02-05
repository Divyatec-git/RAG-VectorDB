from app.embeddings import embed_text

import requests
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
from app.vectordb import index

clientData = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



def retrieve(query: str, k=4):

    try:
        query_embedding = embed_text([query])[0].tolist()

    
        results = index.query(
            vector=query_embedding,
            top_k=3,
            include_metadata=True
        )
        context_chunks = [
                match["metadata"]["text"]
                for match in results["matches"]
            ]

        
       
        return context_chunks
    except Exception as e:
        print(e,"error---------")
        return ""

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
