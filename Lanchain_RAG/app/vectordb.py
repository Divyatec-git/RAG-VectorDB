from langchain_community.vectorstores import Chroma
from .embeddings import embeddings

def create_vectorstore(documents):
    return Chroma.from_documents(
        documents,
        embeddings,
        persist_directory="chroma_db"
    )
