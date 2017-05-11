import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import *
from googleDrive import *


# TitleBar class (custom)
# Tooltip(minimize, maximize, close)
# Set css to widget, dialog, button
class TitleBar(QtWidgets.QFrame):
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
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
        mainUI.close()

    def show_minimize(self):
        mainUI.showMinimized()

    def show_max_restore(self):
        if(self.maxNormal):
            mainUI.showNormal()
            self.maxNormal = False
            self.maximize.setIcon(QtGui.QIcon('images/maximize.png'))
        else:
            mainUI.showMaximized()
            self.maxNormal = True
            self.maximize.setIcon(QtGui.QIcon('images/maximize.png'))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            mainUI.moving = True
            mainUI.offset = event.pos()

    def mouseMoveEvent(self, event):
        if mainUI.moving:
            mainUI.move(event.globalPos() - mainUI.offset)


class MenuBar(QtWidgets.QFrame):
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # set css for TitleBar
        css = """
        QWidget{
            Background: #4374D9;
            border-radius: 0px;
        }
        QMenu{
            color:black;
            Background:#FFFFFF
        }
        QPushButton::menu-indicator{
            image:none;
        }
        QProgressBar {
            background-color:white;
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #05B8CC; 
            width: 20px;
        }
        """

        # set css and background
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)

        # add/remove cloud, setting, arrange button
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setValue(0)  # default

        # set setting button
        self.settingBtn = QtWidgets.QToolButton()
        self.settingBtn.setIcon(QtGui.QIcon('images/setting.png'))
        self.settingBtn.setMouseTracking(True)

        # set array button
        self.arrangeBtn = QtWidgets.QToolButton()
        self.arrangeBtn.setIcon(QtGui.QIcon('images/arrange.png'))

        # add cloud menu
        self.add_menu_setting()

        # remove cloud menu button
        self.removeCloudBtn = QtWidgets.QPushButton()
        self.removeCloudBtn.setIcon(QtGui.QIcon('images/remove_cloud.png'))

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(QtWidgets.QLabel("     "))
        self.layout.addWidget(self.arrangeBtn)
        self.layout.addWidget(self.addCloudBtn)
        self.layout.addWidget(self.removeCloudBtn)
        self.layout.addWidget(self.settingBtn)

        # add action
        self.arrangeBtn.clicked.connect(self.directory_arrange_action)

        # set alignment
        self.layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # set title bar size
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maxNormal = False

    def add_menu_setting(self):
        self.addMenu = QtWidgets.QMenu()
        # set add action
        self.googleAddAction = QtWidgets.QAction(QtGui.QIcon('images/google_small.png'), 'GoogleDrive', self)
        self.boxAddAction = QtWidgets.QAction(QtGui.QIcon('images/box.png'), "Box", self)
        self.dropboxAddAction = QtWidgets.QAction(QtGui.QIcon('images/dropbox.png'), "Dropbox", self)

        self.addMenu.addAction(self.googleAddAction)
        self.addMenu.addAction(self.boxAddAction)
        self.addMenu.addAction(self.dropboxAddAction)

        # add cloud menu button
        self.addCloudBtn = QtWidgets.QPushButton()
        self.addCloudBtn.setIcon(QtGui.QIcon('images/add_cloud.png'))
        self.addCloudBtn.setMenu(self.addMenu)


    def directory_arrange_action(self):
        print("arrange")

    # progressbar's color, percent
    def set_progressbar(self, value):
        self.progressBar.setValue(value)
        if value > 80:
            self.progressBar.setStyleSheet("""
            QProgressBar {
                background-color:white;
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: red; 
                width: 20px;
            }""")
        elif value > 50:
            self.progressBar.setStyleSheet("""
            QProgressBar {
                background-color:white;
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #orange; 
                width: 20px;
            }""")
        else:
            self.progressBar.setStyleSheet("""
            QProgressBar {
                background-color:white;
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC; 
                width: 20px;
            }""")


class StatusBar(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
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

        self.statusLabel = QtWidgets.QLabel("running")

        # set horizontal box
        # add/remove cloud, setting button
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.statusLabel)
        # set title bar size
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maxNormal = False


class DirectoryViewer(QtWidgets.QFrame):
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        css = """
        QFrame{
            Background : #FFFFFF;
            Color:black;
        }
        """
        self.setStyleSheet(css)
        self.setMinimumSize(800, 400)
        self.setAcceptDrops(True)

        box = QtWidgets.QHBoxLayout(self)
        self.label1 = QtWidgets.QLabel("virtual directory")
        box.addWidget(self.label1)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            for url in event.mimeData().urls():
                print(str(url.toLocalFile()))
                print(url.toDisplayString())
                currentfile = QFile(url.toLocalFile())



class MainFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        css = """
        QFrame{
            Background:  #CFCFCF;
            color:white;
            font:13px ;
            font-weight:bold;
            }
        """
        self.setStyleSheet(css)
        self.m_mouse_down = False
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

        self.m_titleBar = TitleBar(self)
        self.m_content = QtWidgets.QWidget(self)
        self.m_menuBar = MenuBar(self)
        self.m_directoryViewer = DirectoryViewer(self)
        self.m_statusBar = StatusBar(self)
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.addWidget(self.m_menuBar)
        vbox.addWidget(self.m_directoryViewer)
        vbox.addWidget(self.m_statusBar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.menubar_action()

    def content_widget(self):
        return self.m_content

    def title_bar(self):
        return self.m_titleBar

    def mousePressEvent(self, event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = (event.button() == Qt.LeftButton)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()

    def mouseReleaseEvent(self, event):
        m_mouse_down = False

    def menubar_action(self):
        # set trigger to action
        self.m_menuBar.googleAddAction.triggered.connect(self.google_drive_clicked)
        self.m_menuBar.boxAddAction.triggered.connect(self.box_clicked)
        self.m_menuBar.dropboxAddAction.triggered.connect(self.dropbox_clicked)

    def google_drive_clicked(self):
        print("google drive added")
        self.m_statusBar.statusLabel.setText("Google Added")
        # do something with browser
        # get return value

    def box_clicked(self):
        print("box added")
        # do something with browser
        # get return value

    def dropbox_clicked(self):
        print("dropbox added")
        # do something with browser
        # get return value


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainFrame()
    mainUI.move(60, 60)
    mainUI.show()
    app.exec_()
