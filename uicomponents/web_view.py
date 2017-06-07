import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *


class WebView(QWebEngineView):
    localhost = ["localhost", "http://localhost", "https://localhost"]
    receive_url_signal = QtCore.pyqtSignal(str, str, str)

    def __init__(self, parent):
        super(WebView, self).__init__()
        self.type = parent[0]
        self.name = parent[1]
        self.setUrl(QUrl(parent[2]))
        self.urlChanged.connect(self.url_changed)

    def change_url(self, url):
        self.setUrl(url)

    def url_changed(self, url):
        current_url = QUrl.host(url)
        for localhostUrls in self.localhost:
            if current_url.startswith(localhostUrls):
                # TODO finish google authorization
                self.receive_url_signal.emit(self.type, self.name, url.toString())
                self.close()
