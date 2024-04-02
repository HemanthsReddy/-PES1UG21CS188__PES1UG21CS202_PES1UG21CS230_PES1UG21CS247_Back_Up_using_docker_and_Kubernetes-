import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def authenticate():
    """Authenticate with Google Drive API using credentials from JSON file."""
    # Specify the path to your JSON credentials file
    json_credentials_path = 'backup_service.json'

    # Load credentials from JSON file
    creds = Credentials.from_service_account_file(json_credentials_path)

    # Build service object for Google Drive API
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_to_drive(file_path, folder_id=None):
    """Upload a file to Google Drive."""
    service = authenticate()

    # Prepare metadata for the file
    file_metadata = {
        'name': os.path.basename(file_path)
    }
    if folder_id:
        file_metadata['parents'] = [folder_id]

    # Upload the file
    media = MediaFileUpload(file_path)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File uploaded successfully with ID:', file.get('id'))

if __name__ == '__main__':
    # Example usage
    file_path = '/path/to/your/file.txt'  # Replace with the path to your file
    folder_id = 'your_folder_id'  # Replace with the ID of the folder in Google Drive (if uploading to a specific folder)
    upload_file_to_drive(file_path, folder_id)
