from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.schemas import DataRecords

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "knowledge_hub"

async def init_mongo():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client[DB_NAME], document_models=[DataRecords])
    print("Beanie ODM initialized with MongoDB")
