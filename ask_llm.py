from langchain_community.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import openai

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

#MDB
mongo_uri = os.getenv("MONGO_URI")
CONNECTION_STRING = str(mongo_uri)
DB_NAME = "demo_rag_insurance"
COLLECTION_NAME = "claims_final"
INDEX_NAME = "vector_index_claim_description"
MongoClient = MongoClient(CONNECTION_STRING)
collection = MongoClient[DB_NAME][COLLECTION_NAME]

#Embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=350, disallowed_special=())


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

def vector_search(mdb_uri, db_name, collection_name, index_name, embeddings, text_path, embedding_path, question, k):
    
    search = MongoDBAtlasVectorSearch.from_connection_string(
        mdb_uri,
        db_name + "." + collection_name,
        embeddings,
        index_name=index_name,
        text_key=text_path, #name of the field to be vectorized
        embedding_key=embedding_path #name of the field to store the embeddings
    )
    
    result = search.similarity_search(question, k)

    for doc in result:
        del doc.metadata['damageDescriptionEmbedding']
    
    return result

def interrogate_llm(question):
    
    vector_search_result = vector_search(mongo_uri, DB_NAME, COLLECTION_NAME, INDEX_NAME, embeddings, "claimDescription", "claimDescriptionEmbedding", question, 3)

    response = ask_openai(question, vector_search_result)

    return response



#Possible prompts and contexts
#context = "To calculate repair time use claimFNOLdate as start date and claimCloseDate as end date."
#context = "I had an accident because of a flat tire. Tell me the average repair time for this claim based on similar claims. To calculate repair time use claimFNOLdate as start date and claimCloseDate as end date."
#context = "I had an accident because of a flat tire."

#question = "Calculate the average loss amount for the accidents and summarize similar accidents."
#question = "Find accidents caused by adverse weather. Tell me the average repair time for this claim based on similar claims. To calculate repair time use claimFNOLdate as start date and claimCloseDate as end date. tell me about the accidents"

#response = interrogate_llm(question)



