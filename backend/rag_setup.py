from get_db import get_database
from storing import get_data, split_image
from chunking import get_chunks
from rag_model import Rag

from superduper import Schema, Table
from superduper.components.schema import FieldType
from superduper import logging
from superduper import ObjectModel
from superduper.components.datatype import file_lazy
from superduper.components.vector_index import sqlvector

from superduper import VectorIndex

from bedrock.embeddings import BedrockCohereEnglishEmbeddings
from bedrock.chat_completion import BedrockAnthropicChatCompletions

from superduper import Plugin
from utils import Processor

from superduper import Table

# Based on https://github.com/superduper-io/superduper/blob/main/templates/pdf_rag/build.ipynb
def rag_setup(mongodb_uri: str, artifact_store: str, pdf_folder: str,
             aws_access_key_id: str, aws_secret_access_key: str, aws_region: str,
             embedding_model: str, chat_completion_model: str,
             source_collection_name: str = "source"):
    
    # Get the database
    db = get_database(mongo_uri=mongodb_uri, artifact_store=artifact_store)
    logging.info(f"Getting data...")

    # Get the data
    data = get_data(pdf_folder=pdf_folder)
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
    coll = Table(identifier=source_collection_name, schema=schema)
    logging.info("Collection:")
    logging.info(coll)

    logging.info(f"Storing source data...")
    db.apply(coll, force=True)
    db[source_collection_name].insert(data).execute()

    # Split the PDF file into images for later result display
    model_split_image = ObjectModel(
        identifier="split_image",
        object=split_image,
        datatype=file_lazy,
    )

    listener_split_image = model_split_image.to_listener(
        key="file",
        select=db[source_collection_name].find(),
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
        select=db[source_collection_name].select(),
        flatten=True,
    )
    db.apply(listener_chunk, force=True)

    # Build a vector index for vector search
    model_embedding = BedrockCohereEnglishEmbeddings(
        identifier='text-embedding',
        foundation_model=embedding_model,
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
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

    chat_completion = BedrockAnthropicChatCompletions(
        identifier='chat-completion',
        foundation_model=chat_completion_model,
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    prompt_template = (
        "The following is a document and question\n"
        "Only provide a very concise answer\n"
        "Context:\n\n"
        "{context}\n\n"
        "Here's the question:{query}\n"
        "answer:"
    )

    rag = Rag(identifier="rag", llm_model=chat_completion, vector_index_name=vector_index.identifier, prompt_template=prompt_template, db=db, processor=processor)
    db.apply(rag, force=True)

    return db, rag

