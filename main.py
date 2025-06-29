from fastapi import FastAPI
from routes.chroma_routes import router as chroma_router
from setup.mongo import init_mongo
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_mongo()

app.include_router(chroma_router)

# any file in the images folder is accessible at http://localhost:8000/images/{filename}.
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI"}
