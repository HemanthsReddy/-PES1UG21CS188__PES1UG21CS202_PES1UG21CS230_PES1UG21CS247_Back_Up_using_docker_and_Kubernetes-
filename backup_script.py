import os
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the scopes required for Google Drive API access
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    """Authenticate with Google Drive API using OAuth 2.0 credentials."""
    try:
        
        credentials = None
        credentials_path = 'backup-service.json'

        if os.path.exists("api_tokens.json"):
            credentials = Credentials.from_authorized_user_file("api_tokens.json", SCOPES)

        if not credentials or not credentials.valid:
            # if credentials and credentials.expired and credentials.refresh_token:
            #     credentials.refresh(Request())
            # else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            credentials = flow.run_local_server(port=0)
            with open("api_tokens.json", "w") as token:
                token.write(credentials.to_json())
        # print(credentials)
        service = build('drive', 'v3', credentials=credentials)

        logging.info("Authentication with Google Drive API successful.")

        return service

    except Exception as e:
        # Log authentication error
        # print("hello")
        logging.error(f"Error during authentication: {str(e)}")
        return None

def upload_file_to_drive(file_path, folder_id=None):
    """Upload a file to Google Drive."""
    try:
        file_name = os.path.basename(file_path)
        service = authenticate()

        # Prepare metadata for the file
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        # Check if file already exists in Google Drive
        results = service.files().list(q=f"name='{file_name}'", fields='files(id)').execute()
        existing_files = results.get('files', [])
        if existing_files:
            # If file exists, get its ID and update it
            file_id = existing_files[0]['id']
            logging.info(f"File '{file_name}' already exists in Google Drive. Updating...")
            media = MediaFileUpload(file_path)
            updated_file = service.files().update(fileId=file_id, media_body=media).execute()
            logging.info(f"File '{file_name}' updated successfully.")
        else:
            # If file doesn't exist, upload it as a new file
            logging.info(f"Uploading file '{file_name}' to Google Drive...")
            media = MediaFileUpload(file_path)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            logging.info(f"File '{file_name}' uploaded successfully with ID: {file.get('id')}")

    except Exception as e:
        # Log file upload error
        logging.error(f"Error uploading file '{file_name}': {str(e)}")
        raise


if __name__ == '__main__':
    # Example usage
    file_path = 'test.txt'  # Replace with the path to your file
    folder_id = ''  # Replace with the ID of the folder in Google Drive (if uploading to a specific folder)
    upload_file_to_drive(file_path, folder_id)
