from __future__ import print_function

import datetime
import pickle
import os.path
import os
import time
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from googleapiclient.http import MediaFileUpload

from model.gdrive_config_model import GDriveConfigModel
from utils import dateutils


class GDriveApi:
    gdrive_config: GDriveConfigModel
    service = Resource

    def __init__(self, config: GDriveConfigModel):
        self.gdrive_config = config
        self.service = self.init_api()

    def upload_file(self, filename, path):
        self.init_api()
        print("Trying upload " + filename + " at path " + path)

        file_metadata = {
            'name': filename,
            'parents': ['appDataFolder']
        }
        media = MediaFileUpload(self.get_file(path), mimetype='application/zip')

        file = self.service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id'
                                      ).execute()
        print('File ID: %s' % file.get('id'))

    def list_files(self):
        # Call the Drive v3 API
        results = self.service.files().list(
            spaces='appDataFolder',
            q="name contains 'tar.gz'", pageSize=30,
            fields="nextPageToken, files(id, name, createdTime)").execute()
        return results.get('files', [])

    def print_list(self):
        items = self.list_files()
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1}) {2}'.format(item['name'], item['id'], item['createdTime']))

    def get_oldest_file(self):
        files = self.list_files()
        oldest_date = None
        oldest_file = None
        for file in files:
            created_time = file['createdTime']
            created_time_date = dateutils.str_to_date_object(created_time)
            if oldest_file is None:
                oldest_file = file
                oldest_date = created_time_date
                continue
            if created_time_date < oldest_date:
                oldest_file = file
                oldest_date = created_time_date
        return oldest_file

    def init_api(self):

        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.gdrive_config.TOKEN_PICK_PATH):
            with open(self.gdrive_config.TOKEN_PICK_PATH, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.gdrive_config.CREDENTIAL_PATH, self.gdrive_config.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.gdrive_config.TOKEN_PICK_PATH, 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        return service

    def delete_file(self,file_id):
        self.service.files().delete(fileId=file_id).execute()

    def remove_oldest_file(self):
        print('Deleting old backup from drive ',self.get_oldest_file())
        self.delete_file(self.get_oldest_file()['id'])

    def get_file(self, path):
        file = open(path)
        print(os.path.basename(file.name))
        print(file.name)
        return file.name
