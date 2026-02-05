from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from .config import settings

def get_embeddings():
    """
    Returns the HuggingFace embeddings model.
    """
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

def get_vectorstore():
    """
    Returns the Chroma vector store.
    """
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=settings.CHROMA_DB_DIR,
        embedding_function=embeddings
    )

def get_rag_chain():
    """
    Creates and returns the RAG chain.
    """
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever()
    
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=settings.MODEL_NAME,
        temperature=0
    )
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    from langchain.prompts import PromptTemplate

    # Custom prompt to restrict answers to the context
    template = """Use the following pieces of context to answer the question at the end.
    If the answer is not in the context, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    return chain
