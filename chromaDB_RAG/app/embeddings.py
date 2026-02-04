from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def embed_text(texts: list[str]):
    return embedding_model.encode(
        texts,
        show_progress_bar=False
    )


# Why this model?
# Free
# Runs on CPU
# 384-dim vectors
# Excellent for RAG