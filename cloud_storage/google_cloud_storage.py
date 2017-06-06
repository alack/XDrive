from __future__ import print_function

import sys

import httplib2
import os
import io
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload, MediaFileUpload

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json


class google_storage_controller:
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = {
        "installed":
        {
            "client_id":"520415020989-j0t973a1oft0anlkan9j3qe6qg4nqme8.apps.googleusercontent.com",
            "project_id":"xdrive-167710",
            "auth_uri":"https://accounts.google.com/o/oauth2/auth",
            "token_uri":"https://accounts.google.com/o/oauth2/token",
            "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
            "client_secret":"A72x7a00FSdsnAZnGNDgk55z",
            "redirect_uris":
            [
                "urn:ietf:wg:oauth:2.0:oob",
                "http://localhost"
            ]
        }
    }
    APPLICATION_NAME = 'XDrives'

    def __init__(self):
        pass

    def authenticate(self):
        """Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'client_secret.json')
        #credential_path =

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def download(drive_service, file_id):
        request = drive_service.files().get_media(fileId=file_id)
        # if get by file
        # fh = io.FileIO('yahoo.jpg', 'wb')

        # get by bytes
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        f = open('asdfaa.jpg', 'wb')
        # save to file
        f.write(fh.getvalue())

    def upload(drive_service):
        file_metadata = {'name': 'photo.jpg'}
        media = MediaFileUpload('photo.jpg', mimetype='image/jpeg')
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))

    def filelist(drive_service):
        results = drive_service.files().list(
            pageSize=100, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))


def main():
    gsc = google_storage_controller()
    credentials = gsc.authenticate()

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # gsc.filelist(service)
    gsc.download(service, '0B3ftHXkfc1YjSWxnWlFtTzdfYzQ')
    # gsc.upload(service)


if __name__ == '__main__':
    main()