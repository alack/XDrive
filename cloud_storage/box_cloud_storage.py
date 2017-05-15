from __future__ import print_function, unicode_literals
# -*- coding: utf-8 -*-
#box fetch시 oauth, download, upload 가능 버전
'''
oauth = OAuth2(
    client_id='8smc0zf5584m4sxgae6d3py7imjvnv4l',
    client_secret='hsrvglivqTNl21CIyBeMVjZu8FYW90A4',
    access_tokens='v9vE8RjLzohJbxji7cV8AvKG1t4Zb0ZN',
)'''

from boxsdk import OAuth2, Client
import bottle
import os
from threading import Thread, Event
import webbrowser
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server


class box_storage_controller:
    client_id = ''  # Insert Box client ID here
    client_secret = ''  # Insert Box client secret here
    access_token = ''
    refresh_token = ''
    client = 0

    def __init__(self, json_data):
        self.client_id = json_data['CLIENT_ID']

    def set_client(self, clientid, clientsecret):
        self.client_id = clientid
        self.client_secret = clientsecret

    def set_token(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret

    def authenticate(self, oauth_class=OAuth2):
        class StoppableWSGIServer(bottle.ServerAdapter):
            def __init__(self, *args, **kwargs):
                super(StoppableWSGIServer, self).__init__(*args, **kwargs)
                self._server = None

            def run(self, app):
                server_cls = self.options.get('server_class', WSGIServer)
                handler_cls = self.options.get('handler_class', WSGIRequestHandler)
                self._server = make_server(self.host, self.port, app, server_cls, handler_cls)
                self._server.serve_forever()

            def stop(self):
                self._server.shutdown()

        auth_code = {}
        auth_code_is_available = Event()

        local_oauth_redirect = bottle.Bottle()

        @local_oauth_redirect.get('/')
        def get_token():
            auth_code['auth_code'] = bottle.request.query.code
            auth_code['state'] = bottle.request.query.state
            auth_code_is_available.set()

        local_server = StoppableWSGIServer(host='localhost', port=8080)
        server_thread = Thread(target=lambda: local_oauth_redirect.run(server=local_server))
        server_thread.start()

        oauth = oauth_class(
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        auth_url, csrf_token = oauth.get_authorization_url('http://localhost:8080')
        print(auth_url)
        webbrowser.open(auth_url)

        auth_code_is_available.wait()
        local_server.stop()
        assert auth_code['state'] == csrf_token
        access_token, refresh_token = oauth.authenticate(auth_code['auth_code'])

        print('access_token: ' + access_token)
        print('refresh_token: ' + refresh_token)

    def upload(self, client):
        root_folder = client.folder(folder_id='0')
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
        a_file = root_folder.upload(file_path, file_name='i-am-a-file.txt')
        try:
            print('{0} uploaded: '.format(a_file.get()['name']))
        finally:
            # print('Delete i-am-a-file.txt succeeded: {0}'.format(a_file.delete()))
            print('super power')

    def download(self, client):
        root_folder = client.folder(folder_id='0')
        items = root_folder.get_items(limit=100)
        print('This is the first 100 items in the root folder:')
        for item in items:
            print("id : "+item.id+"   name : "+item.name)

        f = open(items[1].name, 'wb')
        f.write(client.file(items[1].id).content())
        f.close()
        '''try:
            print('{0} uploaded: '.format(a_file.get()['name']))
        finally:
            # print('Delete i-am-a-file.txt succeeded: {0}'.format(a_file.delete()))
            print('super power')'''

    def test_run(self, oauth, access_token, refresh_token):
        client = Client(oauth)
        # self.upload(client)
        self.download(client)

