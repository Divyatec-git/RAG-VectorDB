import re

def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\x00", "", text)

    return text.strip()
# Why cleaning matters
# ❌ Raw PDFs contain:
# Broken line breaks
# Extra spaces
# Null bytes
# ✅ Cleaning improves:
# Chunk quality
# Embedding accuracy
# Retrieval relevance