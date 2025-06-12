from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from formatting import process_related_documents

from pdf_rag import PDFRag

from superduper import logging

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

# Global dictionaries for caching
db_cache = {}
model_rag_cache = {}

def get_cache_key(industry: str, demo_name: str):
    """Generate a unique cache key based on industry and demo_name."""
    return f"{industry}_{demo_name}"

def set_db(industry, demo_name, db_instance):
    """Store the db instance in the cache."""
    global db_cache
    key = get_cache_key(industry, demo_name)
    db_cache[key] = db_instance

def get_db(industry, demo_name):
    """Retrieve the db instance from the cache."""
    global db_cache
    key = get_cache_key(industry, demo_name)
    return db_cache.get(key)

def set_model_rag(industry, demo_name, model_rag_instance):
    """Store the model_rag instance in the cache."""
    global model_rag_cache
    key = get_cache_key(industry, demo_name)
    model_rag_cache[key] = model_rag_instance

def get_model_rag(industry, demo_name):
    """Retrieve the model_rag instance from the cache."""
    global model_rag_cache
    key = get_cache_key(industry, demo_name)
    return model_rag_cache.get(key)

@app.get("/")
async def read_root(request: Request):
    return {"message":"Server is running"}

@app.post("/cleandb")    
async def clean_db_endpoint(request: Request):   
    data = await request.json()
    industry = data.get("industry")
    demo_name = data.get("demo_name")

    pdf_r = PDFRag(industry=industry, demo_name=demo_name)

    logging.info("Industry:")
    logging.info(pdf_r.industry)
    logging.info("Demo:")
    logging.info(pdf_r.demo_name)

    logging.info("Cleaning up database...")
    pdf_r.clean_db()

    # Making sure I am using global variables
    global db_cache, model_rag_cache

    # Clear cached variables for the specific industry and demo_name
    key = get_cache_key(industry, demo_name)
    if key in db_cache:
        del db_cache[key]
        logging.info(f"Cleared db cache for {industry} - {demo_name}")
    else:
        logging.info(f"No db_cache found for {industry} - {demo_name}")
    if key in model_rag_cache:
        del model_rag_cache[key]
        logging.info(f"Cleared model_rag cache for {industry} - {demo_name}")
    else:
        logging.info(f"No model_rag_cache found for {industry} - {demo_name}")
    
    return {"message": "Database has been successfully cleaned!"}   

@app.post("/setuprag")    
async def setup_rag_endpoint(request: Request):
    data = await request.json()
    industry = data.get("industry")
    demo_name = data.get("demo_name")

    pdf_r = PDFRag(industry=industry, demo_name=demo_name)

    # Check and create the folders
    pdf_r.check_and_create_folders()

    # Download the PDF files from the S3 bucket if enabled
    if pdf_r.aws_s3_enabled or pdf_r.aws_s3_enabled == "True":
        logging.info(f"AWS_S3_ENABLED is {pdf_r.aws_s3_enabled}")
        logging.info("Downloading PDF files from S3 bucket...")
        pdf_r.download_pdf_files_from_s3()
    else:
        logging.info(f"AWS_S3_ENABLED is {pdf_r.aws_s3_enabled}")
        logging.info("Skipping download from S3 bucket...")

    logging.info("Industry:")
    logging.info(pdf_r.industry)
    logging.info("Demo:")
    logging.info(pdf_r.demo_name)
        
    # Check if db and model_rag are already cached
    db_instance = get_db(pdf_r.industry, pdf_r.demo_name)
    model_rag_instance = get_model_rag(pdf_r.industry, pdf_r.demo_name)

    if not db_instance or not model_rag_instance:
        logging.info("Setting up...")  
        # Initialize db and model_rag if not cached
        db_instance, model_rag_instance = pdf_r.setup_rag()
        # Store them in the cache
        set_db(industry, demo_name, db_instance)
        set_model_rag(industry, demo_name, model_rag_instance)
    else:
        logging.info("Using cached instances...")
    
    return {"message": "Database and Model RAG have been successfully set!"}

@app.post("/querythepdf")
async def query_db_endpoint(request: Request):
    data = await request.json()
    industry = data.get("industry")
    demo_name = data.get("demo_name")
    query = data.get("query")
    guidelines = data.get("guidelines")

    # Check if model_rag is cached
    model_rag_instance = get_model_rag(industry, demo_name)
    if model_rag_instance is None:
        return {"message": "Make sure to execute 1. /cleandb and 2. /setuprag before running queries!"}

    try:
        result = model_rag_instance.predict(query, guidelines, top_k=7, format_result=True)
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
        logging.error("Error during prediction:", str(e))
        raise HTTPException(status_code=500, detail="Error processing the request")
