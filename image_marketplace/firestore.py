import uuid
import firebase_admin
from .apps import ImageMarketplaceConfig
from firebase_admin import firestore, storage
from google.api_core.exceptions import NotFound
from google.cloud.exceptions import GoogleCloudError


class FireStorage:
    def __init__(self):
        self.FILE_PATH_KEY = 'local_path'
        self.METADATA_KEY = 'metadata'
        self.BUCKET_NAME = 'shopify-developer-challe-a806f.appspot.com'

        if not firebase_admin._apps:
            self.FIREBASE_APP = firebase_admin.initialize_app()
        else:
            self.FIREBASE_APP = firebase_admin.get_app()
            
        self.bucket = storage.bucket(name=self.BUCKET_NAME, app=self.FIREBASE_APP)


    def upload_files(self, file_records):
        try:
            results = []

            for file_record in file_records:
                file_path = self.upload_file(file_record)
                results.append(file_path)

            return results

        except GoogleCloudError as e:
            raise e


    def upload_file(self, file_record):
        try:
            filename = str(uuid.uuid4())
            file_path = file_record[self.FILE_PATH_KEY]
            file_metadata = file_record[self.METADATA_KEY]

            blob = self.bucket.blob(filename)
            blob.metadata = file_metadata
            blob.upload_from_filename(file_path)
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
