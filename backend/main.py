from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from dotenv import load_dotenv
from db_clean import delete_collections_except_default
from formatting import process_related_documents
from db_setup import setup_db

from superduper import logging

load_dotenv()

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter()

# Global variables for caching
db = None
model_rag = None

@app.get("/")
async def read_root(request: Request):
    return {"message":"Server is running"}

@app.post("/cleandb")    
async def clean_db_endpoint(request: Request):   
    logging.info("Cleaning up database...")
    delete_collections_except_default()
    return {"message": "Database has been successfully cleaned!"}   

@app.post("/setupdb")    
async def setup_db_endpoint(request: Request):
    global db, model_rag    
    logging.info("Setting up database...")    
    db, model_rag = setup_db()
    return {"message": "Database has been successfully created!"}   

@app.post("/querythepdf")
async def query_db(request: Request):
    global model_rag
    if model_rag is None:
        return {"message": "Make sure to execute 1. /cleandb and 2. /setupdb before running queries!"}
    
    data = await request.json()
    query = data.get("query")
    
    try:
        result = model_rag.predict(query, top_k=5, format_result=True)
        logging.info("Response Answer:")
        logging.info(result["answer"])
        logging.info("Response Images:")
        logging.info(result["images"])
        
        # Process the images to extract relevant information
        supporting_docs = process_related_documents(result["images"])
        
        # Return the answer and supporting documents
        return {
            "answer": result["answer"],
            "supporting_docs": supporting_docs
        }

    except Exception as e:
        print("Error during prediction:", str(e))
        raise HTTPException(status_code=500, detail="Error processing the request")
