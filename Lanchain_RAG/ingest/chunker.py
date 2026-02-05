from .tokenizer import tokenizer

def chunk_text(text, chunk_size=500, overlap=100):
    tokens = tokenizer.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk = tokenizer.decode(tokens[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
