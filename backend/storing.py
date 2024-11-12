import os
from dotenv import load_dotenv
from superduper import logging
from superduper import Schema, Table
from superduper import ObjectModel
from superduper.components.datatype import file_lazy
from pdf2image import convert_from_path
from utils import get_file_path

load_dotenv()

PDF_PATH = os.environ.get("PDF_PATH")
PDF_IMAGES = os.environ.get("PDF_IMAGES")
PDF_IMAGES_FOLDER = os.environ.get("PDF_IMAGES_FOLDER")

COLLECTION_NAME = "source"

ROOT_FILE_PATH = get_file_path()

####################
# Create a table to store PDFs.
####################

def get_data(pdf_path: str = PDF_PATH):

    # Concatenating current file path with pdf path
    pdf_folder = ROOT_FILE_PATH + pdf_path
    logging.info(f"PDF Folder: {pdf_folder}")

    pdf_names = [pdf for pdf in os.listdir(pdf_folder) if pdf.endswith(".pdf")]
    logging.info(f"PDF Names: {pdf_names}")

    pdf_paths = [os.path.join(pdf_folder, pdf) for pdf in pdf_names]

    data = [{"url": pdf_path, "file": pdf_path} for pdf_path in pdf_paths]

    return data

####################
# Split the PDF file into images for later result display
####################

def split_image(pdf_path):
    logging.info(f"Splitting images from {pdf_path}")

    image_folders = ROOT_FILE_PATH + PDF_IMAGES
    
    pdf_name = os.path.basename(pdf_path)
    logging.info(f"PDF Name: {pdf_name}")

    images = convert_from_path(pdf_path)
    logging.info(f"Number of images: {len(images)}")

    image_folder = os.path.join(image_folders, pdf_name)
    logging.info(f"Image Folder: {image_folder}")

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    data = []
    for i, image in enumerate(images):
        path = os.path.join(image_folder, f"{i}.jpg")   
        image.save(os.path.join(path))
        data.append(path)
    return data

