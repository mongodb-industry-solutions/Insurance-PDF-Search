from langchain_openai import OpenAIEmbeddings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
#https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['demo_rag_insurance']
collection = db['claims_final']

#embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=2048)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=350)
########################################################################################

""" for document in collection.find():
    #Adds the claim description embedding
    claimDescription = document.get('claimDescription')
    claimDescriptionEmbedding = embeddings.embed_query(claimDescription)
    collection.update_one({'_id': document['_id']}, {'$set': {'claimDescriptionEmbedding': claimDescriptionEmbedding}})

    #Adds the damage description embedding
    damageDescription = document.get('damageDescription')
    damageDescriptionEmbedding = embeddings.embed_query(damageDescription)
    collection.update_one({'_id': document['_id']}, {'$set': {'damageDescriptionEmbedding': damageDescriptionEmbedding}})

    print("Document " + str(document["_id"]) + " updated.")

print("Embeddings created.")
 """

#https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/
def vector_query(embeddings, field, query, index, numCandidates, limit):
    result = db.claims_final.aggregate([
        {
            "$vectorSearch": {
                "index": index,
                "path": field,
                "queryVector": query,
                "numCandidates": numCandidates,
                "limit": limit
            }
        }
    ])
    return result

query = "I had an accident because of a flat tire."
index = "vector_index_claim_description"
numCandidates = 5
limit = 3
field = "claimDescriptionEmbedding"
result = vector_query(embeddings, field, embeddings.embed_query(query), index, numCandidates, limit)
for x in result:
  print(x['claimDescription'])