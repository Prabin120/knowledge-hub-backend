# FastAPI + LangChain + ChromaDB Example

This project demonstrates a FastAPI application with LangChain and ChromaDB integration.

## Features
- FastAPI web server
- LangChain for LLM-based chains (OpenAI example)
- ChromaDB for vector storage and retrieval

## Setup
1. Ensure Python 3.8+
2. Install dependencies:
   ```sh
   pip install fastapi uvicorn[standard] langchain chromadb
   ```
3. Set your OpenAI API key as an environment variable if using the LangChain endpoint:
   ```sh
   set OPENAI_API_KEY=your-key-here
   ```

## Run the server
```sh
uvicorn main:app --reload
```

## Endpoints
- `GET /` — Welcome message
- `POST /langchain-demo/` — Run a LangChain LLM chain (requires `prompt` parameter)
- `POST /chromadb-demo/` — Add/query ChromaDB (requires `item` parameter)
