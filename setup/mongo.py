from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Dict, Any
import os
import sys
import asyncio

# Configuration
MONGO_URL = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "knowledge_hub")
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Global database instance
client: Optional[AsyncIOMotorClient] = None
db = None

async def init_mongo() -> AsyncIOMotorClient:
    """
    Initialize MongoDB connection with retry logic.
    Returns the database instance if successful.
    """
    global client, db
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"Attempting to connect to MongoDB (Attempt {attempt}/{MAX_RETRIES})...")
            
            # Create a new client and connect to the server
            client = AsyncIOMotorClient(
                MONGO_URL,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=30000,         # 30 second connection timeout
                socketTimeoutMS=45000           # 45 second socket timeout
            )
            
            # Test the connection
            await asyncio.wait_for(client.admin.command('ping'), timeout=5.0)
            
            # Get the database
            db = client[DB_NAME]
            print(f"✅ Successfully connected to MongoDB at {MONGO_URL}")
            
            # Create indexes if needed
            # await db.your_collection.create_index("field_name")
            
            return db
            
        except asyncio.TimeoutError:
            print(f"⚠️ Connection attempt {attempt} timed out")
        except Exception as e:
            print(f"⚠️ Connection attempt {attempt} failed: {str(e)}")
        
        if attempt < MAX_RETRIES:
            print(f"Retrying in {RETRY_DELAY} seconds...")
            await asyncio.sleep(RETRY_DELAY)
    
    print("❌ Failed to connect to MongoDB after multiple attempts")
    print("\nTroubleshooting tips:")
    print("1. Make sure MongoDB is installed and running")
    print("2. Check if the MongoDB service is started")
    print("3. Verify the connection string: ", MONGO_URL)
    print("4. If using Docker, ensure the container is running")
    print("5. Check if any firewall is blocking the connection\n")
    
    # Continue running without MongoDB if it's not critical
    # Remove this line if MongoDB is required
    return None

async def close_mongo():
    """Close the MongoDB connection"""
    global client
    if client is not None:
        client.close()
        print("MongoDB connection closed")
