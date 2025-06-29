import pytesseract
from PIL import Image
import aiofiles
from models.schemas import DataRecords
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from setup.chroma import config_collections, error_collections
from io import BytesIO
from globals import model

async def extract_text_from_image(img_path: str) -> str:
    if not img_path:
        return ""
    async with aiofiles.open(img_path, "rb") as f:
        img_bytes = await f.read()
    img = Image.open(BytesIO(img_bytes))
    img = img.convert("RGB")
    text = pytesseract.image_to_string(img)
    return text.strip()

def get_embedding_doc(data: DataRecords, description: str = "") -> Document:
    doc = Document(
        page_content=description,
        metadata={
            "type": getattr(data, "type", None),
            "file_name": data.file_name,
            "config_name": data.config_name,
            "field_configured": data.field_configured,
            "images": data.images
        }
    )
    return doc

async def get_brief_description(data: DataRecords, image: str = "") -> str:
    prompt = PromptTemplate(
        template="""You are a helpful assistant who is helping out to manage a huge number of configurations. \
        Provide a brief description to make vector embedding based on the below data:\n\n
        xml_filename: {file_name}\n\nconfig_name: {config_name}\n\nfield_configured: {field_configured}\n\n
        description: {description}\n\nscreenshot detail of the configuration screen in text: {image}\n""",
        input_variables=["file_name", "config_name", "field_configured", "description", "image"]
    )
    parser = StrOutputParser()
    chain = prompt | model | parser
    res = await chain.ainvoke({
        "file_name": data.file_name,
        "config_name": data.config_name,
        "field_configured": data.field_configured,
        "description": data.description,
        "image": image
    })
    return res

async def saving_config_data(data: DataRecords):
    # If data.images is a list, extract text from each and join
    if isinstance(data.images, list):
        image_texts = []
        for img_path in data.images:
            text = await extract_text_from_image(img_path)
            image_texts.append(text)
        image_text = "\n".join(image_texts)
    else:
        image_text = await extract_text_from_image(data.images)
    brief_description = await get_brief_description(data, image_text)
    doc = get_embedding_doc(data, brief_description)
    doc.page_content = brief_description
    doc.metadata["brief_description"] = brief_description
    # Ensure you pass the correct arguments to ChromaDB
    result = await config_collections.aadd(
        ids=[str(data.id)],
        documents=[brief_description],
        metadatas=[doc.metadata]
    )
    return result