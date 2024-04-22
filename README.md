# Insurance-PDF-Search

### Data Preparation
Create a file named '.env' and store your OpenAI API key and MongoDB connection string in it. A sample has been provided in '.envsample'. Follow this format:

```bash
OPENAI_API_KEY=<your key>
MONGODB_URI=mongodb+srv://user:pass@cluster/db
```

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

``` bash  
pip install -r requirements.txt
```

#### Parse the pdfs and add model in database

```
python sddb.py --init
```

#### Ask your PDF Sample Queries

```
python sddb.py --query "What is a Certificate of Insurance?
python sddb.py --query "what strategy should an insurer first determine?"
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