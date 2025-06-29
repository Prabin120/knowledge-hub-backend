from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp


# model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
model = LlamaCpp(
    model_path="./ai_models/mistral/mistral-7b-instruct.Q4_K_M.gguf",
    temperature=0.7,
    max_tokens=512,
    top_p=0.95,
    n_ctx=2048,
    verbose=True
)
# embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en",
    model_kwargs={"device": "cpu"},  # change to 'cuda' if you use GPU
    encode_kwargs={"normalize_embeddings": True}
)