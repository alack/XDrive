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
        self.url = QUrl(parent[2])
        if self.type == "Dropbox":
            self.setUrl(QtCore.QUrl("https://www.dropbox.com/logout"))
            self.loadFinished.connect(self.load_finished)
        else:
            self.setUrl(self.url)
            self.urlChanged.connect(self.url_changed)

    def load_finished(self, ok):
        self.setUrl(self.url)
        self.urlChanged.connect(self.url_changed)
        self.loadFinished.disconnect()

    def url_changed(self, url):
        current_url = url.toString()
        for localhostUrls in self.localhost:
            if current_url.startswith(localhostUrls):
                self.receive_url_signal.emit(self.type, self.name, url.toString())
                self.close()
