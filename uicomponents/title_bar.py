from PyQt5 import QtWidgets, QtCore, QtGui


class TitleBar(QtWidgets.QFrame):
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # set css for TitleBar
        css = """
        QWidget{
            Background: #F6F6F6;
            color:Black;
            font:12px bold;
            font-weight:bold;
            border-radius: 1px;
            height: 11px;
        }
        QDialog{
            font-size:12px;
            color: black;
        }
        QToolButton{
            Background:#F6F6F6;
            font-size:11px;
        }
        QToolButton:hover{
            font-size:11px;
        }
        QLabel{
            font-size:14px;
        }
        """
        # set css and background
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)
        self.setAcceptDrops(False)

        # XDrive icon
        XD = QtWidgets.QToolButton(self)
        XD.setIcon(QtGui.QIcon('images/xd_blue.png'))

        # tooltip button setting
        self.minimize = QtWidgets.QToolButton(self)
        self.minimize.setIcon(QtGui.QIcon('images/minimize.png'))

        self.maximize = QtWidgets.QToolButton(self)
        self.maximize.setIcon(QtGui.QIcon('images/maximize.png'))

        self.close = QtWidgets.QToolButton(self)
        self.close.setIcon(QtGui.QIcon('images/close.png'))

        # title bar default setting
        self.minimize.setMinimumHeight(15)
        self.close.setMinimumHeight(10)
        self.maximize.setMinimumHeight(10)

        # set title
        label = QtWidgets.QLabel(self)
        label.setText("XDrive")
        self.setWindowTitle("XDrive")

        # set horizontal box for titlebar
        # add label, tooltip buttons
        title_bar_left_layout = QtWidgets.QHBoxLayout()
        title_bar_left_layout.addWidget(XD)
        title_bar_left_layout.addWidget(label)

        title_bar_right_layout = QtWidgets.QHBoxLayout()
        title_bar_right_layout.addWidget(self.minimize)
        title_bar_right_layout.addWidget(self.maximize)
        title_bar_right_layout.addWidget(self.close)

        title_bar_layout = QtWidgets.QHBoxLayout(self)
        title_bar_layout.addLayout(title_bar_left_layout)
        title_bar_layout.addLayout(title_bar_right_layout)

        # set title bar size
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maxNormal = False

        self.close.clicked.connect(self.close_window)
        self.minimize.clicked.connect(self.show_minimize)
        self.maximize.clicked.connect(self.show_max_restore)

    def close_window(self):
        self.parent().close()

    def show_minimize(self):
        self.parent().showMinimized()

    def show_max_restore(self):
        if(self.maxNormal):
            self.parent().showNormal()
            self.maxNormal = False
            self.maximize.setIcon(QtGui.QIcon('images/maximize.png'))
        else:
            self.parent().showMaximized()
            self.maxNormal = True
            self.maximize.setIcon(QtGui.QIcon('images/maximize.png'))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.parent().moving = True
            self.parent().offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.parent().moving:
            self.parent().move(event.globalPos() - self.parent().offset)
