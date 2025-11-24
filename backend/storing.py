import os
from superduper import logging
from pdf2image import convert_from_path
from utils import get_file_path

####################
# Create a table to store PDFs.
####################

def get_data(pdf_folder: str):
    """ Get data from the PDF path 
    Args:
        pdf_path (str): The path to the PDF file.
    Returns:
        list: A list of dictionaries containing the URL and file path.
    """
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

    # Split the path to get the base path up to the dynamic parts
    base_path = os.path.dirname(pdf_path)
    logging.info(f"Base Path: {base_path}")

    # Navigate two levels up
    base_path_two_levels_up = os.path.abspath(os.path.join(base_path, '..', '..'))
    logging.info(f"Base Path Two Levels Up: {base_path_two_levels_up}")

    # Construct the pdf_images_path path by appending '/pdf-images'
    pdf_images_path = os.path.join(base_path_two_levels_up, 'pdf-images')
    # PDF Images Path: /Users/julian.boronat/Github/mongodb/mongodb-industry-solutions/cross-backend-rag/backend/data/fsi/leafy_bank_assistant/pdf-images
    image_folders = pdf_images_path
    logging.info(f"Image Folders: {image_folders}")
    
    pdf_name = os.path.basename(pdf_path)
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

