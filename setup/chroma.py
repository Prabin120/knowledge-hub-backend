import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import EmbeddingFunction
from typing import List, Union
from globals import embedding_model

# Create a wrapper class for HuggingFace embeddings
class HuggingFaceEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model):
        self.model = model

    def __call__(self, texts: Union[str, List[str]]) -> List[List[float]]:
        if isinstance(texts, str):
            texts = [texts]
        # Convert to list of strings if needed
        texts = [str(text) for text in texts]
        # Get embeddings
        embeddings = self.model.embed_documents(texts)
        return embeddings

# Initialize the embedding function
hf_embedding_function = HuggingFaceEmbeddingFunction(embedding_model)

# Singleton ChromaDB client setup
chroma_client = chromadb.Client(Settings(persist_directory="knowledge_hub"))

# Get or create collections with the custom embedding function
config_collections = chroma_client.get_or_create_collection(
    "config_collections",  # Fixed typo in collection name
    embedding_function=hf_embedding_function
)

error_collections = chroma_client.get_or_create_collection(
    "error_collections",
    embedding_function=hf_embedding_function
)
