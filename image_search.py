from torchvision import transforms as ts
import torchvision.models as models
from pymongo import MongoClient
from PIL import Image
import base64
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
CONNECTION_STRING = str(mongo_uri)
MongoClient = MongoClient(CONNECTION_STRING)
db = MongoClient['claim_resolution']
coll = db['car_damage_photos']

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

    image.save("frontend/public/car_damage/test.jpg", format="JPEG")

    

    query_image = 'frontend/public/car_damage/test.jpg'
    image_folder = 'car_damage/'
    query_embedding = image_vectorizer.vectorize(query_image).tolist()

    documents = coll.aggregate([
                {
                "$search": {
                "index": "default",
                "knnBeta": {
                "vector": query_embedding,
                "path": "embedding",
                "k": 5
                }
                }
                }
                ])

    documents = list(documents)  

    similar_images_list = []

    for i in range (5):
        image_file = documents[i]['filename']
        image_path = os.path.join(image_folder, image_file)
        similar_images_list.append(image_path)

    #reset test image
    if os.path.exists('frontend/public/car_damage/test.jpg'):
        os.remove('frontend/public/car_damage/test.jpg')
    
    return similar_images_list
