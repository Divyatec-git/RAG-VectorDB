import sys
import os

# Add the project root to python path
sys.path.append('/home/divya/Divya/vector/rag_chatbot/langchain_rag_app')

try:
    from app.main import app
    from app.rag import get_embeddings
    print("Successfully imported app and rag modules.")
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
