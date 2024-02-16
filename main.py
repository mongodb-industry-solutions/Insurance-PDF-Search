from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.schema import Document
from langchain_community.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

CONNECTION_STRING = str(mongo_uri)
DB_NAME = "demo_rag_insurance"
COLLECTION_NAME = "claims_final"
INDEX_NAME = "vector_index_claim_description"
#INDEX_NAME = "default"


MongoClient = MongoClient(CONNECTION_STRING)
collection = MongoClient[DB_NAME][COLLECTION_NAME]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=350, disallowed_special=())
#embeddings = OpenAIEmbeddings(model="text-embedding-ada-002-v2", dimensions=350)

vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    CONNECTION_STRING,
    DB_NAME + "." + COLLECTION_NAME,
    embeddings,
    index_name=INDEX_NAME,
    text_key="claimDescription",
    embedding_key="claimDescriptionEmbedding"
)

query = "I had an accident because of a flat tire."

results = vector_search.similarity_search(
    query=query, k=5)

# Display results
for result in results:
    print(result)