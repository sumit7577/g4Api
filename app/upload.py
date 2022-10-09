import os
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContentSettings
from azure.storage.blob import BlobClient


MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=ituksodevstorage;AccountKey=nehryycawKQGXrBQL1fDFFLgEzDOsj4bccBdUW+xOeX+BFopElaKgyEQ74xuKhlLwKbUOn3g7tOalnNgsAxGfg==;EndpointSuffix=core.windows.net"
MY_CONTAINER = "video-frozenbrothers"

# Replace with the local folder which contains the files for upload
LOCAL_PATH = "blobupload/"


class AzureBlobFileUploader:
    def __init__(self):
        print("Intializing AzureBlobFileUploader")

        # Initialize the connection to Azure storage account
        self.blob_service_client = BlobServiceClient.from_connection_string(
            MY_CONNECTION_STRING)

    def upload_file(self, file_name):
        blob_client = self.blob_service_client.get_blob_client(container=MY_CONTAINER,
                                                               blob=file_name)
        upload_file_path = os.path.join(LOCAL_PATH, file_name)

        # Create blob on storage
        # Overwrite if it already exists!
        file_content_setting = ContentSettings(content_type='/h264')
        print(f"uploading file - {file_name}")
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(
                data, overwrite=True, content_settings=file_content_setting)

    def download_file(self,fileName:str):
        blob_client = BlobClient.from_connection_string(MY_CONNECTION_STRING,MY_CONTAINER,fileName)
        with open("./name.txt", "wb") as my_blob:
            blob_data = blob_client.download_blob()
            blob_data.readinto(my_blob)


# Initialize class and upload files

azure_blob_file_uploader = AzureBlobFileUploader()
