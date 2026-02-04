import tiktoken

encoder = tiktoken.get_encoding("cl100k_base")

def chunk_text(text, chunk_size=800, overlap=100):
    tokens = encoder.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = encoder.decode(chunk_tokens)

        chunks.append(chunk_text)
        start += chunk_size - overlap

    return chunks

# Chunking rules (industry standard)
# 300–800 tokens per chunk
# 50–150 token overlap
# Why overlap?
# Because meaning often spans chunk boundaries.