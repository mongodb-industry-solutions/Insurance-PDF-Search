from langchain_openai import OpenAIEmbeddings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os
#import openai
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
""" try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e) """

db = client['demo_rag_insurance']
collection = db['claims_final']

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=2048)
########################################################################################

for document in collection.find():
    
    claimDescription = document.get('claimDescription')
    claimDescriptionEmbedding = embeddings.embed_query(claimDescription)
    collection.update_one({'_id': document['_id']}, {'$set': {'claimDescriptionEmbedding': claimDescriptionEmbedding}})

    damageDescription = document.get('damageDescription')
    damageDescriptionEmbedding = embeddings.embed_query(damageDescription)
    collection.update_one({'_id': document['_id']}, {'$set': {'damageDescriptionEmbedding': damageDescriptionEmbedding}})

    print("Document " + str(document["_id"]) + " updated.")

print("Embeddings created.")