# Insurance-PDF-Search

### Add environment variables

> **_Note:_** Create a .env file within the backend directory.

```bash
MONGODB_URI=
ARTIFACT_STORE=data/guidlines/artifacts
IMAGES_FOLDER=data/guidlines/images
USE_OPENAI=TRUE
TITLE="SuperDuperDB / Insurance Guidlines: AI Search & RAG Chat (OpenAI)"
OPENAI_API_KEY=
```

### Generate a venv for the Backend

Change directory:

```
cd backend
```

Create virtual environment in Python:

```
python3 -m venv virtualBack
```

Activate Virtual environment:

```
source virtualBack/bin/activate
```

Install Python dependencies:

```
pip install -r requirements.txt
```

Start the server:

```
python3 -m uvicorn main:app --reload
```

### Data Preparation

In MongoDB Atlas create a databse called "demo_rag_insurance" and a collection called "claims_final", import the dataset "demo_rag_insurance.claims.json" into the collection. You have to create two Vector Search Indexes, one for "claimDescriptionEmbedding" called "vector_index_claim_description" and one for "photoEmbedding" called "default":

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "claimDescriptionEmbedding",
      "numDimensions": 350,
      "similarity": "cosine"
    }
  ]
}
```

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "photoEmbedding",
      "numDimensions": 1000,
      "similarity": "cosine"
    }
  ]
}
```

run

```bash
pip install -r requirements.txt
```

#### Parse the pdfs and add model in database

At this point you can either analyze and index the PDFs yourself running the script below, or simply create a new database called "insurance_pdf_search" and import all the collections contained in the folder "insurance_pdf_search_db". If you're indexing the PDFs yourself, once the script is done, import "customer.json" to your database (contained in the "insurance_pdf_search_db" folder).

```
python3 sddb.py --init
```
Add the vector index on the collection "_output.elements.chunk" and the field "_outputs.elements.text-embedding-ada-002.0":

```json
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "_outputs.elements.text-embedding-ada-002.0",
      "similarity": "cosine",
      "type": "vector"
    },
    {
      "path": "_outputs.elements.chunk.0.source_elements.metadata.filename",
      "type": "filter"
    }
  ]
}
```
#### Ask your PDF Sample Queries

```
python3 sddb.py --query "What is a Certificate of Insurance?"
python3 sddb.py --query "what strategy should an insurer first determine?"
```

and now, launch the backend

```bash
python3 -m uvicorn main:app --reload
```

move to the frontend folder and run the frontend

```bash
npm install
npm start
```

### Build the Application with Docker

To build the Docker images and start the services, run the following command:

```
make build
```

### Stopping the Application

To stop all running services, use the command:

```
make stop
```

### Cleaning Up

To remove all images and containers associated with the application, execute:

```
make clean
```

```

```
