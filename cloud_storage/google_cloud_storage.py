from __future__ import print_function

import sys

import httplib2
import os
import io

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
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = {"installed":{"client_id":"767027085829-0macfn189q3ddpbsi78tdg4ue938k6nv.apps.googleusercontent.com","project_id":"opportune-ego-163505","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://accounts.google.com/o/oauth2/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"HjXDJKdLgz8eRbWVAMBq7w5N","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}
APPLICATION_NAME = 'djsc023401'


def get_credentials():
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
    credential_path = os.path.join(credential_dir, 'djsc023401.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
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
    credentials = get_credentials()

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # filelist(service)
    download(service, '0B3ftHXkfc1YjSWxnWlFtTzdfYzQ')
    # upload(service)


if __name__ == '__main__':
    main()