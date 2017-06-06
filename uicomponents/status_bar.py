from PyQt5 import QtWidgets, QtGui, QtCore


class StatusBar(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # set css for TitleBar
        css = """
        QWidget{
            Background: #F6F6F6;
            border-radius: 1px;
            color: black;
        }
        """
        # set css and background
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)

        self.statusIconBtn = QtWidgets.QToolButton()
        self.statusIconBtn.setIcon(QtGui.QIcon('images/status_ok.png'))
        self.statusLabel = QtWidgets.QLabel("running")

        # set horizontal box
        # add/remove cloud, setting button
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.statusIconBtn)
        hbox.addWidget(self.statusLabel)
        # set title bar size
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maxNormal = False

    def set_status_label(self, msg):
        self.statusLabel.setText(msg)

    def set_status_ok(self, msg):
        self.statusIconBtn.setIcon(QtWidgets.QIcon('images/status_ok.png'))
        self.set_status_label(msg)

    def set_status_wait(self, msg):
        self.statusIconBtn.setIcon(QtWidgets.QIcon('images/status_wait.png'))
        self.set_status_label(msg)

    def set_status_fail(self, msg):
        self.statusIconBtn.setIcon(QtWidgets.QIcon('images/status_fail.png'))
        self.set_status_label(msg)
