from __future__ import print_function, unicode_literals
#code that use restful box api is unsuccessful
"""
import os
import webbrowser
import http.server
import urllib.request
import threading
from threading import Event


class box_cloud_storage:
    # self : function
    # client_id
    # client_secret
    # token(opt., dic{'access': 'string', 'refresh': 'string'})
    httpd = http.server.HTTPServer(('localhost', 8080), http.server.SimpleHTTPRequestHandler)

    def __init__(self, client_id, client_secret, token):
        print('Hello world!!!!!')
        ip, port = self.httpd.server_address
        server_thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True

        auth_code_is_available = Event()

        local_oauth_redirect =

        @local_oauth_redirect.get('/')
        def get_token():
            auth_code['auth_code'] = bottle.request.query.code
            auth_code['state'] = bottle.request.query.state
            auth_code_is_available.set()

        server_thread.start()
        print('Server loop running in thread:')
        url = "https://account.box.com/api/oauth2/authorize\
         ?response_type=code&client_id=" + client_id + "\
         &redirect_uri=localhost:8080&state=ppap"
        req = urllib.request.Request(url)
        print(req)
        data = urllib.request.urlopen(req).read()
        print('Receive : ', data)
        f = open("./response_iphone.html", 'wb')
        f.write(data)
        f.close()

        auth_code_is_available.wait()
        self.httpd.shutdown()
        print('Hello world')
        self.httpd.server_close()


        # if token['access'] != '' and token['refresh'] != '':
        # access access_token 보내보고 받아오는 답이 이상하면
        #    a = "https: //api.box.com/oauth2/revoke \
        #    -d client_id=" + client_id+" -d client_secret="+client_secret+" \
        #    -d token="+token['access']+" -X POST"
        # access refresh_token 보내보고 받아오는 답이 이상하면
        #    a = "https: //api.box.com/oauth2/revoke \
        #    -d client_id=" + client_id+" -d client_secret="+client_secret+" \
        #    -d token="+token['refresh']+" -X POST"
        # client_id, client_secret을 보내서 auth를 수행한다.

    def upload_box(self):
        #upload file
        return 10

    def download_box(self):
        #download file
        return 10

    '''first, read auth_file then check the box client_id and client_secret
   second, if box client_id & client_secret == existance
   '''

def main():
    CLIENT_ID = 'dzoi6w486bus5wxah249kazsbb9bg2jl'  # Insert Box client ID here
    CLIENT_SECRET = '4hfnl7Dv601JyfawLHXxEFbqwipMJ6mb'  # Insert Box client secret here
    tok={'access':'', 'refresh':''}
    bcs = box_cloud_storage('kfjsdhfaskgasd',CLIENT_SECRET,tok)

if __name__ == '__main__':
    main()
"""


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
import json
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server

BOX_CONFIG_FILE = './data/idpw.json'


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

    def upload_file(self, client):
        root_folder = client.folder(folder_id='0')
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
        a_file = root_folder.upload(file_path, file_name='i-am-a-file.txt')
        try:
            print('{0} uploaded: '.format(a_file.get()['name']))
        finally:
            # print('Delete i-am-a-file.txt succeeded: {0}'.format(a_file.delete()))
            print('super power')

    def download_file(self, client):
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
        # upload_file(client)
        self.download_file(client)


def main():
    storage_names = ['BOX', 'GOOGLE', 'DROPBOX']
    f = open(BOX_CONFIG_FILE, 'r')
    json_data = json.loads(f.read())
    f.close()
    storage = [[]]
    for storage_name in storage_names
        for i in range(0, json_data[storage_name]['CNT']):
            storage[storage_name][i] = box_storage_controller(json_data[storage_name]['LIST'][i])
            box[i].authenticate()
            box[i].test_run()
    os._exit(0)


if __name__ == '__main__':
    main()


