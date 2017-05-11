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

    """first, read auth_file then check the box client_id and client_secret
   second, if box client_id & client_secret == existance
   """













def main():
    CLIENT_ID = 'dzoi6w486bus5wxah249kazsbb9bg2jl'  # Insert Box client ID here
    CLIENT_SECRET = '4hfnl7Dv601JyfawLHXxEFbqwipMJ6mb'  # Insert Box client secret here
    tok={'access':'', 'refresh':''}
    bcs = box_cloud_storage('kfjsdhfaskgasd',CLIENT_SECRET,tok)

if __name__ == '__main__':
    main()
