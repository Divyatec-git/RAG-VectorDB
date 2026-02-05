import os

def load_documents(folder):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r") as f:
                docs.append(f.read())
    return docs
