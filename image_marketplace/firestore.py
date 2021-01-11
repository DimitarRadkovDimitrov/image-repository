import uuid
import firebase_admin
from .apps import ImageMarketplaceConfig
from firebase_admin import firestore, storage
from google.api_core.exceptions import NotFound
from google.cloud.exceptions import GoogleCloudError


class FireStorage:
    def __init__(self):
        if not firebase_admin._apps:
            self.FIREBASE_APP = firebase_admin.initialize_app()
        else:
            self.FIREBASE_APP = firebase_admin.get_app()
            
        self.BUCKET_NAME = 'shopify-developer-challe-a806f.appspot.com'
        self.bucket = storage.bucket(name=self.BUCKET_NAME, app=self.FIREBASE_APP)


    def upload_file(self, path_to_image, file_metadata=None):
        try:
            filename = str(uuid.uuid4())
            blob = self.bucket.blob(filename)
            blob.metadata = file_metadata
            blob.upload_from_filename(path_to_image)
            return filename

        except GoogleCloudError as e:
            raise e


    def delete_file(self, blob_id):
        try:
            blob = self.bucket.blob(blob_id)
            blob.delete()

        except NotFound as e:
            raise e

        except GoogleCloudError as e:
            return e
