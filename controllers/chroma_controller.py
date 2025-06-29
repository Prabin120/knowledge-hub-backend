from fastapi import HTTPException
from setup.chroma import config_collections, error_collections
from models.schemas import DataRecords, GetInfoRequest
from utils.mongo import get_collection
import asyncio
import base64
import os
import uuid

from ai.save_config import saving_config_data
from utils.saving_image import save_base64_image

IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

async def upload_data_controller(request: dict):
    print("Received request:", request)
    try:
        id = str(uuid.uuid4())
        # Save image and get path
        image_path = await save_base64_image(base64_str=request["image"], file_name=id+".png", save_dir=IMAGES_DIR)
        # Prepare document for MongoDB
        doc = {
            "_id": id,
            "type": request["type"],
            "file_name": request["file_name"],
            "config_name": request["config_name"],
            "field_configured": request.get("field_configured", []),
            "description": request.get("description", ""),
            "image_filepath": image_path
        }
        collection = get_collection()
        await collection.insert_one(doc)
        await saving_config_data(DataRecords(**doc))
        return {"message": "Document uploaded successfully.", "id": id, "image_filepath": image_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# async def query_data(request: GetInfoRequest):
#     try:
#         query = request.query
#         type = request.type
#         if type == "configuration":
            
#         n_results = request.n_results
#         results = await config_collections.find({"$text": {"$search": query}}).to_list(length=n_results)
#         return results
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))