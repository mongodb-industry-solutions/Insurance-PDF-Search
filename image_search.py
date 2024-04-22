from torchvision import transforms as ts
import torchvision.models as models
from pymongo import MongoClient
from PIL import Image
import base64
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")
CONNECTION_STRING = str(mongo_uri)
MongoClient = MongoClient(CONNECTION_STRING)
#db = MongoClient['claim_resolution']
#coll = db['car_damage_photos']
db = MongoClient['demo_rag_insurance']
coll = db['claims_final']

class ImageVectorizer:
    def __init__(self):
        self.normalize = ts.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        )
        # https://pytorch.org/vision/0.8/models.html
        self.model = models.squeezenet1_0(pretrained=True, progress=False)

    def vectorize(self, image_file_name):
        image = Image.open(image_file_name).convert("RGB")
        image = ts.Resize(256)(image)
        image = ts.CenterCrop(224)(image)
        tensor = ts.ToTensor()(image)
        tensor = self.normalize(tensor).reshape(1, 3, 224, 224)
        vector = self.model(tensor).cpu().detach().numpy().flatten()
        return vector
    
def image_search(image):

    image_vectorizer = ImageVectorizer()

    base64_image = image[image.find(",") + 1:]
    bytes_image = base64.b64decode(base64_image)
    image = Image.open(BytesIO(bytes_image))

    if image.format != "JPEG":
        image = image.convert("RGB")

    image.save("frontend/public/photos/test.jpg", format="JPEG")
    query_image = 'frontend/public/photos/test.jpg'
    
    query_embedding = image_vectorizer.vectorize(query_image).tolist()
    limit = 4

    documents = coll.aggregate([
        {
            '$vectorSearch': {
                'index': 'default', 
                'path': 'photoEmbedding', 
                'queryVector': query_embedding, 
                'numCandidates': 20, 
                'limit': limit
            }
        }
        ]) 

    documents = list(documents)  
   
    
    for i in range (limit):
        del documents[i]['damageDescriptionEmbedding']
        del documents[i]['claimDescriptionEmbedding']
        del documents[i]['photoEmbedding']
        del documents[i]['_id']

    #reset test image
    if os.path.exists('frontend/public/photos/test.jpg'):
        os.remove('frontend/public/photos/test.jpg')
    
    return documents
    
