from base import BaseConfig
from rag_setup import rag_setup
from db.clean_db import delete_collections_except_default

from superduper import logging
import logging

from botocore.exceptions import ClientError

import os
from dotenv import load_dotenv

load_dotenv()


class PDFRag(BaseConfig):
    """
    PDFRag class to setup the RAG model for PDFs.
    """

    def __init__(self, *args, **kwargs):
        super(PDFRag, self).__init__(*args, **kwargs)

        # In the expression _aws_s3_enabled = self.demo_config['aws_s3_enabled'] or os.getenv("AWS_S3_ENABLED"), 
        # the value of _mongodb_uri will prioritize mongodb_uri if it is provided and evaluates to a truthy value. 
        # If mongodb_uri is not provided or evaluates to a falsy value (such as None, False, 0, "", etc.), 
        # it will fall back to the value of os.getenv("MONGODB_URI").
        # And the same applies to other variables.
        if self.demo_config['aws_s3_enabled'] is None or self.demo_config['aws_s3_enabled'] == "" or self.demo_config['aws_s3_enabled'] == "False":
            self.aws_s3_enabled = None
        else:
            self.aws_s3_enabled = self.demo_config['aws_s3_enabled'] or os.getenv("AWS_S3_ENABLED")

        if  self.aws_s3_enabled:
             self.aws_s3_bucket = self.demo_config['aws_s3_bucket'] or os.getenv("AWS_S3_BUCKET")
             self.aws_s3_pdf_folder = self.demo_config['aws_s3_pdf_folder'] or os.getenv("AWS_S3_PDF_FOLDER")
        else:
             self.aws_s3_bucket = None
             self.aws_s3_pdf_folder = None

        # Get the current working directory
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
        pdf_folder = self.demo_config['pdf_folder'] or os.getenv("PDF_FOLDER")

        # Set pdf_folder and pdf_images_folder relative to the current directory
        self.pdf_folder = os.path.join(self.current_dir, pdf_folder)

        self.pdfs = self.demo_config['pdfs'] or os.getenv("PDFS")
        self.artifacts_store = self.demo_config['artifacts_store'] or os.getenv("ARTIFACT_STORE")
        self.embedding_model = self.demo_config['embedding_model'] or os.getenv("EMBEDDING_MODEL")
        self.chat_completion_model = self.demo_config['chat_completion_model'] or os.getenv("CHAT_COMPLETION_MODEL")

    def execute(self):
        logging.basicConfig(level=logging.INFO)
        logging.info(f'Industry name: {self.industry}')
        logging.info(f'S3 Bucket: {self.aws_s3_bucket}')
        logging.info(f'S3 PDF folder: {self.aws_s3_pdf_folder}')
        logging.info(f'PDF Folder: {self.pdf_folder}')
        logging.info(f'PDFs: {self.pdfs}')

        # # Clean the database
        # self.clean_db()

        # # Check and create the folders
        # self.check_and_create_folders()

        # # Download the PDF files from the S3 bucket if enabled
        # if self.aws_s3_enabled:
        #     self.download_pdf_files_from_s3()
        
        # db, model_rag = self.setup_rag()

        # question = "<YOUR QUESTION HERE>"
        # result = model_rag.predict(question, format_result=True)
        
        # print("Result:")
        # print(result)
        # print("Answer:")
        # print(result["answer"])

    def clean_db(self):
        """ Clean the database. """
        logging.info("Cleaning up the database...")
        delete_collections_except_default(mongo_uri=self.mdb_uri)
        logging.info(f"Database for {self.industry} - {self.demo_name} has been cleaned.")

    def check_and_create_folders(self):
        """ Check if pdf_folder and pdf_images_folder exist, and create them if they do not. """
        if not os.path.exists(self.pdf_folder):
            os.makedirs(self.pdf_folder)
            logging.info(f'Created folder: {self.pdf_folder}')
        else:
            logging.info(f'Folder already exists: {self.pdf_folder}')

    def get_pdf_files(self):
        """ Get the list of PDF files in the S3 bucket. """
        try:
            pdf_files_list = self.list_s3_objects(bucket=self.aws_s3_bucket, prefix=self.aws_s3_pdf_folder)
            logging.info("List of PDF files in the S3 bucket")
            logging.info(pdf_files_list)
            return pdf_files_list
        except ClientError as e:
            logging.error(e)

    def download_pdf_files_from_s3(self):
        """ Download the PDF files from the S3 bucket."""
        pdf_files = self.get_pdf_files()
        
        # Check if there are no files to download
        if len(pdf_files) <= 1:
            logging.info("No PDF files to download.")
            return

        # Download the PDF files
        # Skip the first file as it is the folder name
        for pdf_file in pdf_files[1:]:
            file_name = pdf_file.split('/')[-1]
            logging.info(f'Downloading PDF file: {pdf_file}')
            destination = os.path.join(self.pdf_folder, file_name)

            # Check if the file already exists
            if os.path.exists(destination):
                logging.info(f'File already exists: {destination}. Skipping download.')
                continue

            self.download_file_from_s3(bucket_name=self.aws_s3_bucket, object_name=pdf_file, filename=destination)
            logging.info(f'Downloaded PDF file: {destination}')

    def setup_rag(self):
        """ Setup the RAG model for PDFs. """
        logging.info("Setting up the RAG model for PDFs...")
        db, model_rag = rag_setup(
            mongodb_uri = self.mdb_uri, 
            artifact_store = self.artifacts_store, 
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key, 
            aws_region = self.aws_region,
            pdf_folder = self.pdf_folder,
            embedding_model = self.embedding_model,
            chat_completion_model = self.chat_completion_model
        )

        return db, model_rag
    