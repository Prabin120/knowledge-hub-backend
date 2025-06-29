from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "knowledge_hub"
COLLECTION_NAME = "data_records"

class MongoDB:
    client: AsyncIOMotorClient = None

mongodb = MongoDB()

def get_collection():
    return mongodb.client[DB_NAME][COLLECTION_NAME]

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(MONGO_URL)
    print("Connected to MongoDB")

async def close_mongo_connection():
    mongodb.client.close()
    print("Closed MongoDB connection")
