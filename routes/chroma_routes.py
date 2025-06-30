from fastapi import APIRouter, HTTPException, Body
from models.schemas import DataRecords, GetInfoRequest
from controllers.chroma_controller import upload_data_controller

router = APIRouter()

@router.post("/upload-data", tags=["chroma"])
async def upload_data(request: dict = Body(...)):
    print("Received request:", request)
    return await upload_data_controller(request)

# @router.post("/get-info", tags=["chroma"])
# async def get_info(request: GetInfoRequest = Body(...)):
#     return get_info_controller(request)
