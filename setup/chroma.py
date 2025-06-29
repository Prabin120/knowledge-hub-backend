import chromadb
from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings
from globals import embedding_model

# Singleton ChromaDB client setup
chroma_client = chromadb.Client(Settings(persist_directory="knowledge_hub"))

# Example: get or create a collection
config_collections = chroma_client.get_or_create_collection(
    "congig_collections",
    embedding_function=embedding_model
)

error_collections = chroma_client.get_or_create_collection(
    "error_collections",
    embedding_function=embedding_model
)
