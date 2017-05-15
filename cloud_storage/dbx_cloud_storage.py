import dropbox
from dropbox.files import WriteMode
from dropbox import DropboxOAuth2FlowNoRedirect

class Dropbox_storage_controller:
    APP_KEY = "cep4re0edd3vsmp"
    APP_SECRET = "7029x3nth5mykw9"
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.TOKEN = "1"

    def dbx_token(self):
        APP_KEY = "cep4re0edd3vsmp"
        APP_SECRET = "7029x3nth5mykw9"
        auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()
        try:
            oauth_result = auth_flow.finish(auth_code)
        except Exception as e:
            print('Error: %s' % (e,))
        self.TOKEN = oauth_result.access_token

    def dbx_upload(self, file_name, upload_path):
        APP_KEY = "cep4re0edd3vsmp"
        APP_SECRET = "7029x3nth5mykw9"
        dbx = dropbox.Dropbox(self.TOKEN)
        with open(file_name, 'rb') as f:
            dbx.files_upload(f.read(), upload_path + file_name, mode=WriteMode('overwrite'))

    def dbx_download(self, file_name, download_path):
        dbx = dropbox.Dropbox(self.TOKEN)
        dbx.files_download_to_file(file_name, download_path + file_name)

