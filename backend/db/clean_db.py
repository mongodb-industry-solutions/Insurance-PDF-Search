from pymongo import MongoClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MongoDBCleanerCollections")

def delete_collections_except_default(mongo_uri: str):
    """
    Delete all collections in a MongoDB database except the 'default' collection.
    
    Args:
        mongo_uri (str): MongoDB URI
        
    Returns:
        None
    """

    log: logging.Logger = logger
    
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
            log.info(f'Deleted collection: {collection}')
        else:
            log.info(f'Skipped collection: {collection}')
    # Close the client connection
    client.close()
