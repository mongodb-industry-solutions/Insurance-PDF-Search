import base64
from io import BytesIO

def convert_image_to_base64(img):
    """Convert an image to a base64."""
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return image_base64

def process_related_documents(images):
    """Process the images to extract related docs and images."""
    supporting_docs = []
    
    for message, img in images:
        full_text = (
            f"**Related docs**: {message}\n\n"
        )
        # Convert the image to base64 if it exists
        image_base64 = convert_image_to_base64(img) if img else None
        supporting_docs.append({
            "full_text": full_text,  # Store the combined text
            "image": image_base64
        })
    
    return supporting_docs