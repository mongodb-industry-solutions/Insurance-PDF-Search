#pip3 install langchain pymongo bs4 openai tiktoken gradio requests lxml argparse unstructured
#openai_api_key = "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" 
#from pymongo import MongoClient

from langchain_openai import OpenAIEmbeddings
#import gradio as gr
#from gradio.themes.base import Base
#import key_param

from dotenv import load_dotenv
import os
import openai
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=2048)
text = "This is a test document."
query_result = embeddings.embed_query(text)
print(len(query_result))