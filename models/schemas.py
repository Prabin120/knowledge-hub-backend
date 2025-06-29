from pydantic import BaseModel, Field
from typing import List, Optional

class GetInfoRequest(BaseModel):
    query: str
    type: str
    image: Optional[str] = None  # Base64 encoded image string

class DataRecords(BaseModel):
    type: str
    file_name: str
    config_name: str
    field_configured: List[str] = []
    description: str = ""
    image_filepath: str

