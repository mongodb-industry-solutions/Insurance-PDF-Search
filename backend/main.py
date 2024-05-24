import os
from io import BytesIO
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from ask_llm import interrogate_llm
from image_search import image_search
import base64

from superduperdb import superduper
#from superduperdb.backends.mongodb import Collection
from sddb import qa
from utils import get_related_merged_documents

load_dotenv()
print("------------------------------------------------------------------------")
print(os.getenv("MONGODB_URI"))
print(os.getenv("ARTIFACT_STORE"))

mongodb_uri = os.getenv("MONGODB_URI")
artifact = os.getenv("ARTIFACT_STORE")
db = superduper(mongodb_uri, artifact_store=f"filesystem://{artifact}")
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@app.get("/")
def root():
    return {"message": "Server is running"}

@app.post("/askTheLlm")
async def ask_llm(request: Request):
    data = await request.json()
    question = data.get("question")
    similar_docs, llm_output = interrogate_llm(question)
    return {"question": question, "result": llm_output, "similar_docs": similar_docs}

@app.post("/imageSearch")
async def find_similar_images(request: Request):
    data = await request.json()
    droppedImage = data.get("droppedImage") 
    similar_documents = image_search(droppedImage)
    return {"similar_documents": similar_documents}
    
@app.post("/querythepdf")
async def query_db(request: Request):
    data = await request.json()
    query = data.get("query")
    guidelines = data.get("guidelines")

    # Log the guidelines file name
    print("Using the file:", guidelines)

    output, out = qa(db, query, guidelines, vector_search_top_k=5)
    supporting_docs = []
    for text, img in get_related_merged_documents(out, output):
        if img:
            #supporting_docs.append({"text": text, "image": FileResponse(img)})
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            supporting_docs.append({"text": text, "image": image_base64})
    toreturnobj = {"answer": output, "supporting_docs": supporting_docs}
    return toreturnobj