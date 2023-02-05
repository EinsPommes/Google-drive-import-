import io
import shutil
import os
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

def upload_folder_to_drive(folder_path, service, folder_name):
    """Uploads a folder to Google Drive.

    folder_path: The local path of the folder to be uploaded.
    service: The Google Drive API service instance.
    folder_name: The name of the folder to be created in Google Drive.
    """
    # Create the folder on Google Drive
    folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = service.files().create(body=folder_metadata, fields='id').execute()

    # Upload the files in the folder to Google Drive
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            media = MediaFileUpload(file_path, mimetype='application/octet-stream')
            file_metadata = {'name': file, 'parents': [folder['id']]}
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f'The folder "{folder_path}" has been successfully uploaded to Google Drive as "{folder_name}"')

def main():
    # Build the Google Drive API client
    service = build('drive', 'v3', developerKey='YOUR_DEVELOPER_KEY')

    # Upload the folder to Google Drive
    folder_path = r'path/to/local/folder'
    folder_name = 'Name of folder on Google Drive'
    upload_folder_to_drive(folder_path, service, folder_name)

if __name__ == '__main__':
    main()