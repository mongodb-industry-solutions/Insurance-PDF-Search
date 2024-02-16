from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.schema import Document
from langchain_community.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
#from langchain_community.vectorstores import MongoDBAtlasVectorSearch
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
COLLECTION_NAME = "test"
INDEX_NAME = "vector_index"

client = MongoClient(CONNECTION_STRING)
collection = client[DB_NAME][COLLECTION_NAME]

from langchain_community.document_loaders import PyPDFLoader

# Load the PDF
loader = PyPDFLoader("https://arxiv.org/pdf/2303.08774.pdf")
data = loader.load()
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1536, disallowed_special=())
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(data)

from langchain_openai import OpenAIEmbeddings

# insert the documents in MongoDB Atlas with their embedding
vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents=docs,
    embedding=embeddings,
    collection=collection,
    index_name=INDEX_NAME,
)

# Perform a similarity search between the embedding of the query and the embeddings of the documents
query = "What were the compute requirements for training GPT 4"
results = vector_search.similarity_search(query)

print(results[0].page_content)