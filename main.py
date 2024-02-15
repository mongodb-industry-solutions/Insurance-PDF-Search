#pip3 install langchain pymongo bs4 openai tiktoken gradio requests lxml argparse unstructured
#from pymongo import MongoClient

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
#https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri, server_api=ServerApi('1'))

db_name = "demo_rag_insurance"
collection_name = "claims_final"
collection = client[db_name][collection_name]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=350)
index_name = "claimDescriptionEmbedding"
vector_field_name = "claimDescriptionEmbedding"
text_field_name = "claimDescription"

#https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.mongodb_atlas.MongoDBAtlasVectorSearch.html
#https://python.langchain.com/docs/integrations/vectorstores/mongodb_atlas
vectorStore = MongoDBAtlasVectorSearch(collection,embeddings, text_field_name, vector_field_name, index_name)
query = "I had an accident and my car was damaged."

result = vector_search.similarity_search(query=query, num_candidates=10, limit=2)