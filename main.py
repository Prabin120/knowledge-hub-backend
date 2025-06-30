from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any
import os

from setup.mongo import init_mongo, close_mongo, db as mongo_db
from routes.chroma_routes import router as chroma_router

# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Knowledge Hub Backend...")
    
    # Initialize MongoDB connection
    db = await init_mongo()
    app.state.mongodb = db  # Store db in app.state
    
    # Check if MongoDB is available
    app.state.mongodb_available = db is not None
    if app.state.mongodb_available:
        print("✅ MongoDB connection established")
    else:
        print("⚠️ Running without MongoDB - some features may be limited")
    
    yield  # Application runs here
    
    # Shutdown
    print("\n🛑 Shutting down...")
    if app.state.mongodb_available:
        await close_mongo()
        print("✅ MongoDB connection closed")

# Initialize FastAPI
app = FastAPI(
    title="Knowledge Hub API",
    description="Backend API for Knowledge Hub application",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    chroma_router,
    prefix="/api/v1",
    tags=["chroma"],
    responses={404: {"description": "Not found"}},
)

# Serve static files from the images directory
app.mount("/images", StaticFiles(directory="images"), name="images")

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Check the health of the API and its dependencies"""
    status = {
        "status": "ok",
        "version": "1.0.0",
        "database": {
            "status": "connected" if app.state.mongodb_available else "disconnected",
            "type": "mongodb"
        }
    }
    
    return status

# Root endpoint
@app.get("/", tags=["root"])
async def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to the Knowledge Hub API",
        "documentation": "/docs",
        "health_check": "/health"
    }
