from langchain_community.vectorstores import Chroma
from .embeddings import embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()


def get_retriever():
    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    return db.as_retriever(search_kwargs={"k": 4})

prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}
""")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)