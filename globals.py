from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp

# Initialize the language model
model = None
try:
    model = LlamaCpp(
        model_path="./ai_models/mistral/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        temperature=0.7,
        max_tokens=512,
        top_p=0.95,
        n_ctx=2048,
        verbose=True
    )
    print("✅ Mistral model loaded successfully")
except Exception as e:
    print(f"⚠️ Failed to load Mistral model: {e}")
    print("⚠️ Some features may not be available without the language model")

# Initialize the embedding model
embedding_model = None
try:
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en",
        model_kwargs={"device": "cpu"},  # change to 'cuda' if you use GPU
        encode_kwargs={"normalize_embeddings": True}
    )
    print("✅ Embedding model loaded successfully")
except Exception as e:
    print(f"⚠️ Failed to load embedding model: {e}")
    print("⚠️ Some features may not be available without the embedding model")