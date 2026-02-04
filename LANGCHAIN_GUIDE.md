# What is LangChain & Why Use It?

You asked about LangChain. Even though this project currently uses "raw" Python to build RAG, LangChain is a very popular framework that automates many of these steps.

This document explains what it is, why people use it, and how it compares to the manual approach.

---

## 1. What is LangChain?

**LangChain** is a library (available in Python and JavaScript) designed to make building AI applications easier. Think of it like **jQuery** or **React** for AI.

*   **Raw Python**: You have to write code to connect to the LLM, format the string for the prompt, parse the output, connect to the database, etc.
*   **LangChain**: Provides pre-built "blocks" for all of these things that you can snap together.

---

## 2. Why Use It? (The Benefits)

### 1. **Component Abstraction (Swap things easily)**
In our current project, if we want to switch from **Google Gemini** to **OpenAI GPT-4**, we have to rewrite our `rag.py` file to change the API calls.
*   **With LangChain**: You just change one line of code:
    ```python
    # Switch from this:
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    # To this:
    llm = ChatOpenAI(model="gpt-4")
    ```
    The rest of your code (prompts, RAG logic) stays exactly the same.

### 2. **Pre-built Chains**
RAG is a common pattern. LangChain has a pre-built function called `RetrievalQA`.
*   **Manual**: We wrote `retrieve()`, `embed()`, `query_db()`, `build_prompt()`.
*   **LangChain**: `chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())`. It does all that work for you.

### 3. **Prompt Management**
It helps organize prompts so they aren't just messy f-strings in your code. It handles variables and formatting cleanly.

---

## 3. How to Use LangChain (Examples)

Here is how you would rebuild parts of our project using LangChain.

### Installation
```bash
pip install langchain langchain-google-genai chromadb
```

### Example 1: Simple Prompting
Instead of formatting strings manually:
```python
from langchain_core.prompts import PromptTemplate

# Define a template with variables
template = PromptTemplate.from_template("Tell me a {adjective} joke about {topic}.")

# Format it
prompt = template.format(adjective="funny", topic="cats")
# Output: "Tell me a funny joke about cats."
```

### Example 2: The RAG Flow (Replacing our `rag.py`)

This is arguably the most powerful part. It replaces 50+ lines of our code with just a few lines.

```python
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# 1. Setup the LLM and Embeddings
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# 2. Connect to ChromaDB (It handles the 'get collection' part)
db = Chroma(persist_directory="./chroma", embedding_function=embeddings)

# 3. Create the RAG Chain
# This one line replaces our entire 'retrieve' and 'answer' functions!
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # "stuff" means "stuff all text into prompt"
    retriever=db.as_retriever()
)

# 4. Ask a question
response = qa_chain.invoke({"query": "How do embeddings work?"})
print(response["result"])
```

---

## 4. Summary: When to use which?

| Feature | Raw Python (Our Project) | LangChain |
| :--- | :--- | :--- |
| **Control** | **High**. You know exactly what happens on every line. | **Medium**. Some magic happens under the hood. |
| **Debugging** | **Easier**. Standard Python errors. | **Harder**. Stack traces can be deep and confusing. |
| **Speed to Build**| Slower. You write everything. | **Fast**. Glue components together. |
| **Integration** | You build connectors manually. | Has 100+ connectors (PDFs, GDrives, Notions, etc). |

**Conclusion:**
For learning (like this project), **Raw Python** is better because you understand *how* it works.
For building complex production apps with many different tools, **LangChain** saves a lot of time.
