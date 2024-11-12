import os
from dotenv import load_dotenv
from utils import get_file_path
from superduper import superduper, CFG
from superduper import logging

load_dotenv()

# How MONGODB_URI must look
# "mongodb+srv://<user>:<password>@ist-shared.n0kts.mongodb.net/<database_name>"
MONGODB_URI = os.getenv('MONGODB_URI')
ARTIFACT_STORE = os.environ.get("ARTIFACT_STORE")

def get_database(mongo_uri: str = MONGODB_URI):
        """ To initialize the database connection
        Args:
            mongo_uri: The connection string URI
        Returns:
            None
        """

        try:
            file_path = get_file_path()

            # Concatenating current file path with pdf path
            artifacts_folder = file_path + ARTIFACT_STORE
            logging.info(f"Artifacts Folder: {artifacts_folder}")

            CFG.bytes_encoding = 'str'
            CFG.native_json = False
            
            db = superduper(mongo_uri, artifact_store=f"filesystem://{artifacts_folder}")
            
            logging.info("Database details:")
            logging.info({db})
            logging.info("Type:")
            logging.info({type(db)})
            
            return db
        except Exception as e:
            raise Exception(
                "The following error occurred: ", e)

def init_app(mongo_uri: str = MONGODB_URI):
    try:
        file_path = get_file_path()

         # Concatenating current file path with pdf path
        artifacts_folder = file_path + ARTIFACT_STORE
        logging.info(f"Artifacts Folder: {artifacts_folder}")
        
        CFG.bytes_encoding = 'str'
        CFG.native_json = False
        
        db = superduper(mongo_uri, artifact_store=f"filesystem://{artifacts_folder}")
        model_rag = db.load("model", "rag")

        return db, model_rag
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)