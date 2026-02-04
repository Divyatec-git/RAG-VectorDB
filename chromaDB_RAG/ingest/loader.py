from pypdf import PdfReader
from pathlib import Path

def load_documents(folder_path: str):
    documents = []

    for file in Path(folder_path).iterdir():
        if file.suffix == ".pdf":
            reader = PdfReader(file)
            for i, page in enumerate(reader.pages):
                documents.append({
                    "text": page.extract_text(),
                    "source": file.name,
                    "page": i + 1
                })

        elif file.suffix == ".txt":
            documents.append({
                "text": file.read_text(),
                "source": file.name,
                "page": None
            })

    return documents
# We separate loading from processing
# Metadata (source, page) is critical later