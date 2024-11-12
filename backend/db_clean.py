from pymongo import MongoClient

import os
from dotenv import load_dotenv
from superduper import logging

load_dotenv()

# How MONGODB_URI must look
# "mongodb+srv://<user>:<password>@ist-shared.n0kts.mongodb.net/<database_name>"
MONGODB_URI = os.getenv('MONGODB_URI')

def delete_collections_except_default(mongo_uri: str = MONGODB_URI):
    # Create a MongoDB client
    client = MongoClient(mongo_uri)
    
    # Access the specified database (the database name is included in the URI)
    db_name = mongo_uri.split('/')[-1]  # Extract the database name from the URI
    db = client[db_name]
    
    # List all collections in the database
    collections = db.list_collection_names()
    
    # Loop through the collections and drop them if they are not 'default'
    for collection in collections:
        if collection != 'default':
            db.drop_collection(collection)
            logging.info(f'Deleted collection: {collection}')
        else:
            logging.info(f'Skipped collection: {collection}')
    # Close the client connection
    client.close()


# if __name__ == '__main__':

#     logging.info("Cleaning up database...")
#     delete_collections_except_default()