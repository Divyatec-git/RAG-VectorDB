from .rag_chain import rag_chain

while True:
    query = input("Ask: ")
    if query == "exit":
        break
    print(rag_chain.invoke(query))
