import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

def tokenize(text):
    return tokenizer.encode(text)
