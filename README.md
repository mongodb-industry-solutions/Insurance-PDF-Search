# Insurance RAG demo - WIP

Create a file named '.env' and store your OpenAI API key and MongoDB connection string in it, follow this format:

```bash
OPENAI_API_KEY=<your key>
MONGO_URI="mongodb+srv://<usr>:<pswd>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority"
```
In MongoDB Atlas create a databse called "demo_rag_insurance" and a collection called "claims_final", import the dataset "demo_rag_insurance.claims.json". You have to create two Vector Search Indexes, one for "claimDescriptionEmbedding" called "vector_index_claim_description" specifying the number of dimensions of our embedding arrays (350 in our case),
the field where the embeddings are stored within our document ("claimDescriptionEmbedding"), and the similarity measure ("cosine", "dotproduct" or "euclidean").
```json
{
  "fields": [
    {
      "numDimensions": 350,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```

``` bash  
pip install -r requirements.txt
```

and then launch the backend

```bash
python3 -m uvicorn main:app --reload
```
move to the frontend folder and run the frontend

```bash
npm install
npm start
```

