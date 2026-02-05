from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import rag_answer

app = FastAPI()

class ChatPayload(BaseModel):
    query: str

@app.post("/chat")
def chat(payload: ChatPayload):
    answer = rag_answer(payload.query)
    return {
        "query": payload.query,
        "answer": answer
    }
