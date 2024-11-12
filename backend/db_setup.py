from spdp import get_database
from storing import get_data, split_image
from chunking import get_chunks
from rag_model import Rag

from superduper import Schema, Table
from superduper.components.schema import FieldType
from superduper import logging
from superduper import ObjectModel
from superduper.components.datatype import file_lazy
from superduper.components.vector_index import sqlvector

from superduper_openai import OpenAIEmbedding
from superduper_openai import OpenAIChatCompletion
from superduper import VectorIndex

from superduper import Plugin
from utils import Processor

from superduper import Table

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_ACCESS_KEY = os.getenv('OPENAI_ACCESS_KEY')
COLLECTION_NAME = "source"

# Based on https://github.com/superduper-io/superduper/blob/main/templates/pdf_rag/build.ipynb
def setup_db():

    db = get_database()
    logging.info(f"Getting data...")
    data = get_data()
    logging.info(f"Data to insert:")
    logging.info(data)

    # Create a table to store PDFs.
    logging.info(f"Getting collection...")

    logging.info("Creating Schema...")
    schema = Schema(identifier="myschema", fields={'url': 'str', 'file': file_lazy})
    logging.info("Schema:")
    logging.info(schema)
    
    logging.info("Creating Collection...")
    # In MongoDB this Table refers to a MongoDB collection, otherwise to an SQL table.
    # https://docs.superduper.io/docs/execute_api/data_encodings_and_schemas#create-a-table-with-a-schema
    coll = Table(identifier=COLLECTION_NAME, schema=schema)
    logging.info("Collection:")
    logging.info(coll)

    logging.info(f"Storing source data...")
    db.apply(coll, force=True)
    db[COLLECTION_NAME].insert(data).execute()

    # Split the PDF file into images for later result display
    model_split_image = ObjectModel(
        identifier="split_image",
        object=split_image,
        datatype=file_lazy,
    )

    listener_split_image = model_split_image.to_listener(
        key="file",
        select=db[COLLECTION_NAME].find(),
        flatten=True,
    )
    db.apply(listener_split_image, force=True)

    # Build a chunks model and return chunk results with coordinate information.
    model_chunk = ObjectModel(
        identifier="chunk",
        object=get_chunks,
        datatype=FieldType(identifier="json")
    )

    listener_chunk = model_chunk.to_listener(
        key="file",
        select=db[COLLECTION_NAME].select(),
        flatten=True,
    )
    db.apply(listener_chunk, force=True)

    # Build a vector index for vector search
    model_embedding = OpenAIEmbedding(
            openai_api_key=OPENAI_ACCESS_KEY,
            identifier='text-embedding-ada-002', 
            datatype=sqlvector(shape=(1536,))
            )

    listener_embedding = model_embedding.to_listener(
        key=f"{listener_chunk.outputs}.txt",
        select=db[listener_chunk.outputs].select(),
    )

    vector_index = VectorIndex(
        identifier="vector-index",
        indexing_listener=listener_embedding,
    )

    db.apply(vector_index, force=True)

    # Create a plugin
    #### When applying the processor, saves the plugin in the database, thereby saving the related dependencies as well.
    #### The processor will integrate the returned chunks information with the images, and return a visualized image.​

    processor = Processor(
        identifier="processor",
        db=db,
        chunk_key=listener_chunk.outputs,
        split_image_key=listener_split_image.outputs,
        plugins=[Plugin(path="./utils.py")],
    )

    # Create a RAG model
    #### Create a RAG model to perform retrieval-augmented generation (RAG) and return the results.
    #### Rag class here: ./rag_model.py
    #### Imported as from rag_model import Rag
    
    llm_openai = OpenAIChatCompletion(openai_api_key=OPENAI_ACCESS_KEY, identifier='llm-openai', model='gpt-3.5-turbo')

    prompt_template = (
        "The following is a document and question\n"
        "Only provide a very concise answer\n"
        "Context:\n\n"
        "{context}\n\n"
        "Here's the question:{query}\n"
        "answer:"
    )

    rag = Rag(identifier="rag", llm_model=llm_openai, vector_index_name=vector_index.identifier, prompt_template=prompt_template, db=db, processor=processor)
    db.apply(rag, force=True)

    return db, rag


# if __name__ == '__main__':

#     logging.info("Setting up database...")
#     setup_db()