from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from .rag import get_retriever
from .rag import prompt
from .rag import llm

retriever = get_retriever()

rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)
