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

MongoClient = MongoClient(CONNECTION_STRING)
collection = MongoClient[DB_NAME][COLLECTION_NAME]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=350)
#embeddings = OpenAIEmbeddings(model="text-embedding-ada-002-v2", dimensions=350)

vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    CONNECTION_STRING,
    DB_NAME + "." + COLLECTION_NAME,
    embeddings,
    index_name=INDEX_NAME,
    text_key="claimDescription",
    embedding_key="claimDescriptionEmbedding"
)

qa_retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5},
)

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=qa_retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
)

#interaction = {"query": "I got a flat tire, can you find claims with similar characteristics and tell me the average loss amount?", "context": "I had an accident because of a flat tire."}
interaction = {"query": "I got a flat tire, summarize similar accidents and tell me the average loss amount as specified in the documents provided", "context": "I had an accident because of a flat tire."}
#interaction = {"query": "Show me the expected repair time for this claim based on similar claims", "context": "I had an accident because of a flat tire."}
#interaction = {"query": "I got a flat tire, summarize similar accidents", "context": "I had an accident because of a flat tire."}

docs = qa(interaction)

#page_content = docs["source_documents"][0].metadata['totalLossAmount']
#page_content = docs["source_documents"][0].metadata['insurableObject']['insurableObjectId']

print(docs['result'])
