from langchain_core.documents import Document
from .loader import load_documents
from .cleaner import clean_text
from .chunker import chunk_text
from app.vectordb import create_vectorstore

def ingest():
    raw_docs = load_documents("data/docs")
    documents = []

    for text in raw_docs:
        cleaned = clean_text(text)
        chunks = chunk_text(cleaned)

        for chunk in chunks:
            documents.append(
                Document(page_content=chunk)
            )

    vectorstore = create_vectorstore(documents)
    vectorstore.persist()
if __name__ == "__main__":
    ingest()
    print("Ingestion completed")