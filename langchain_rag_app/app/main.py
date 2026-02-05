from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import shutil
import os
from .rag import get_rag_chain, get_vectorstore
from .data_processing import clean_text, chunk_text

app = FastAPI(title="LangChain RAG Chatbot")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

# Initialize global RAG chain (can be improved for per-user sessions)
rag_chain = get_rag_chain()

@app.post("/ingest")
async def ingest_text(file: UploadFile = File(...)):
    """
    Ingests a text file or PDF, cleans it, chunks it, and adds it to the vector store.
    """
    try:
        filename = file.filename.lower()
        if filename.endswith(".pdf"):
            import io
            from pypdf import PdfReader
            
            content = await file.read()
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        else:
            # Assume text file
            content = await file.read()
            text = content.decode("utf-8")
        
        cleaned_text = clean_text(text)
        chunks = chunk_text(cleaned_text)
        
        vectorstore = get_vectorstore()
        vectorstore.add_documents(chunks)
        
        return {"message": f"Successfully ingested {len(chunks)} chunks from {file.filename}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """
    Chat endpoint to query the RAG system.
    """
    try:
        # Note: This simple implementation uses a shared memory. 
        # For a real multi-user app, you gain handle sessions differently.
        result = rag_chain.invoke({"question": request.query})
        return QueryResponse(answer=result["answer"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to LangChain RAG Chatbot API"}
