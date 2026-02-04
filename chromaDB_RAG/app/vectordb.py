import chromadb
# from chromadb.config import Settings

# client = chromadb.Client(
#     Settings(
#         persist_directory="./chroma",
#         anonymized_telemetry=False
#     )
# )
client = chromadb.PersistentClient(path="./chroma")


collection = client.get_or_create_collection(
    name="rag_docs"
)


# Why persistence?
# Survives restarts
# No re-embedding
# Scales to 100k+ chunks