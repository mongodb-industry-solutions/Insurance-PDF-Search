from utils import get_file_path
from superduper import superduper, CFG
from superduper import logging

def get_database(mongo_uri: str, artifact_store: str):
    """
    Get the database connection

    Args:
        mongo_uri (str): MongoDB URI
        artifact_store (str): Artifact store path

    Raises:
        Exception: The following error occurred: {e}

    Returns:
        _type_: Database connection
    """
    
    try:
        file_path = get_file_path()

        # Concatenating current file path with artifact store path
        artifacts_folder = f"{file_path}/{artifact_store}"
        logging.info(f"Artifacts Folder: {artifacts_folder}")

        CFG.bytes_encoding = 'str'
        CFG.native_json = False

        db = superduper(
            mongo_uri, artifact_store=f"filesystem://{artifacts_folder}")

        logging.info("Database details:")
        logging.info({db})
        logging.info("Type:")
        logging.info({type(db)})

        return db
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
