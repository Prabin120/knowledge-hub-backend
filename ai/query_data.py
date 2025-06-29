from fastapi import HTTPException
from models.schemas import GetInfoRequest
from setup.chroma import config_collections, error_collections
from utils.saving_image import get_image_from_base64
from globals import model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

async def get_embedded(data: GetInfoRequest):
    """
    Fetch embedded data based on the request.
    """
    try:
        query = data.query
        image = get_image_from_base64(data.image)
        promt = PromptTemplate(
            template="""You are a helpful assistant who is helping out to manage a huge number of configurations. \
            Provide a brief description to make vector embedding based on the below data:\n\n
            query: {query}\n\nScreenshot detail of the configuration screen in text: {image}\n""",
            input_variables=["query", "image"]
        )
        parser = StrOutputParser()
        chain = promt | model | parser
        res = await chain.ainvoke({
            "query": query,
            "image": image
        })
        results = config_collections.query(query_texts=[res], n_results=5)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

async def get_config_info(data: GetInfoRequest):
    """
    Fetch configuration information based on the request.
    """
    try:
        results = await get_embedded(data)
        prompt = PromptTemplate(
            template="""
            You are a helpful assistant who is helping out to manage a huge number of configurations. \
            Provide the right configuration details based on the user query and the embedded data:\n\n
            query: {query}\n\n
            embedded_data: {embedded_data}\n\n
            """,
            input_variables=["query", "embedded_data"]
        )
        parser = StrOutputParser()
        chain = prompt | model | parser
        response = await chain.ainvoke({
            "query": data.query,
            "embedded_data": results
        })
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# async def get_info(request: GetInfoRequest):
#     """
#     Controller to handle the get info request.
#     """
#     try:
#         if request.type == "config":
#             return await get_config_info(request)
#         elif request.type == "error":
#             return await get_error_info(request)
#         else:
#             raise HTTPException(status_code=400, detail="Invalid type specified")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) from e