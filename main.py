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
import openai

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

CONNECTION_STRING = str(mongo_uri)
DB_NAME = "demo_rag_insurance"
COLLECTION_NAME = "claims_final"
INDEX_NAME = "vector_index_claim_description"

MongoClient = MongoClient(CONNECTION_STRING)
collection = MongoClient[DB_NAME][COLLECTION_NAME]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=350, disallowed_special=())
#embeddings = OpenAIEmbeddings(model="text-embedding-ada-002-v2", dimensions=350)

def ask_openai(question, data):
    response = openai.completions.create(model="gpt-3.5-turbo-instruct",  # Choose an appropriate engine for your needs
    prompt=f"{question}\n\nAdditional Information:\n{data}",
    temperature=0.7,
    max_tokens=2000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0)
    # Return the text portion of the response
    return response.choices[0].text.strip()


vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    CONNECTION_STRING,
    DB_NAME + "." + COLLECTION_NAME,
    embeddings,
    index_name=INDEX_NAME,
    text_key="claimDescription",
    embedding_key="claimDescriptionEmbedding"
)

context = "I had an accident because of a flat tire. To calculate repair time use claimFNOLdate as start date and claimCloseDate as end date."
#question = "Calculate the average loss amount for the accidents and summarize similar accidents."
#question = "Tell me the average repair time for this claim based on similar claims."
question = "Tell me the if the customer has a coverages for these kind of accidents."

results = vector_search.similarity_search(
    query=context, k=3)

#Strips embedding from the results to avoid sending it to OpenAI for performance reasons
for doc in results:
    del doc.metadata['damageDescriptionEmbedding']

response = ask_openai(question, results)

print(response)






