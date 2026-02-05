import re
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing excessive newlines and whitespace.
    """
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Chunks the text into smaller documents using RecursiveCharacterTextSplitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    docs = text_splitter.create_documents([text])
    return docs
