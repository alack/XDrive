import sys
import random
from urllib.parse import urlparse
from os.path import splitext
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


# TitleBar class (custom)
# Tooltip(minimize, maximize, close)
# Set css to widget, dialog, button
from PyQt5.QtWidgets import QListView


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

        # set home button
        self.homeBtn = QtWidgets.QToolButton()
        self.homeBtn.setIcon(QtGui.QIcon('images/home.png'))

        # set setting button
        self.settingBtn = QtWidgets.QToolButton()
        self.settingBtn.setIcon(QtGui.QIcon('images/setting.png'))

        # set array button
        self.arrangeBtn = QtWidgets.QToolButton()
        self.arrangeBtn.setIcon(QtGui.QIcon('images/arrange.png'))

        # set add folder button
        self.addFolderBtn = QtWidgets.QToolButton()
        self.addFolderBtn.setIcon(QtGui.QIcon('images/add_folder_blue.png'))

        # add cloud menu
        self.add_menu_setting()

        # remove cloud menu button
        self.removeCloudBtn = QtWidgets.QPushButton()
        self.removeCloudBtn.setIcon(QtGui.QIcon('images/remove_cloud.png'))

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(self.homeBtn)
        self.layout.addWidget(self.addFolderBtn)
        self.layout.addWidget(self.arrangeBtn)
        self.layout.addWidget(self.addCloudBtn)
        self.layout.addWidget(self.removeCloudBtn)
        self.layout.addWidget(self.settingBtn)

        # add action
#        self.arrangeBtn.clicked.connect(self.directory_arrange_action)

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
        QListView{
            Background: #FFFFFF;
        }
        """
        self.setStyleSheet(css)
        self.m_mouse_down = False
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

        self.m_titleBar = TitleBar(self)
        self.m_menuBar = MenuBar(self)
        self.m_statusBar = StatusBar(self)
        self.m_listview = DirectoryView()
        self.model = PiecesModel(self)
        self.m_listview.setModel(self.model)

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.addWidget(self.m_menuBar)
        vbox.addWidget(self.m_listview)
        vbox.addWidget(self.m_statusBar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.menubar_action()

    def title_bar(self):
        return self.m_titleBar

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

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        elif event.mimeData().hasFormat('image/x-puzzle-piece'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            upload_list = event.mimeData().urls()
            count = len(upload_list)
            if count >= 2:
                status = str(count)+" files are uploading"
                self.m_statusBar.statusLabel.setText(status)
            elif count == 1:
                status = str(upload_list[0].toLocalFile())
                self.m_statusBar.statusLabel.setText(str(upload_list[0].toLocalFile())+" is uploading")
            for url in upload_list:
                print(str(url.toLocalFile()))
                path = urlparse(url.toLocalFile()).path
                ext = splitext(path)[1]
                print(ext)
                self.add_icons(ext, event.pos())

        elif event.mimeData().hasFormat('image/x-puzzle-piece'):
            pieceData = event.mimeData().data('image/x-puzzle-piece')
            stream = QDataStream(pieceData, QIODevice.ReadOnly)
            square = self.targetSquare(event.pos())
            pixmap = QPixmap()
            location = QPoint()
            stream >> pixmap >> location
            self.m_listview.pieceLocations.append(location)
            self.m_listview.piecePixmaps.append(pixmap)
            self.m_listview.pieceRects.append(square)
            self.m_listview.hightlightedRect = QRect()
            self.m_listview.update(square)
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            self.m_listview.highlightedRect = QRect()
            event.ignore()

    def find_piece(self, pieceRect):
        try:
            return self.m_listview.pieceRects.index(pieceRect)
        except ValueError:
            return -1

    def mouseReleaseEvent(self, event):
        m_mouse_down = False

    def mousePressEvent(self, event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = (event.button() == Qt.LeftButton)

    def add_icons(self, ext, pos):
        if ext == ".md":
            image = QPixmap('images/folder.png')
        elif ext == ".png":
            image = QPixmap('images/box.png')
        else:
            image = QPixmap('images/close_after.png')
        self.model.addPieces(image)


class PiecesModel(QAbstractListModel):
    def __init__(self, parent=None):
        super(PiecesModel, self).__init__(parent)
        self.locations = []
        self.pixmaps = []

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.DecorationRole:
            return QIcon(self.pixmaps[index.row()].scaled(
                60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        if role == Qt.UserRole:
            return self.pixmaps[index.row()]

        if role == Qt.UserRole + 1:
            return self.locations[index.row()]

        return None

    def addPiece(self, pixmap, location):
        row = len(self.pixmaps)
        self.beginInsertRows(QModelIndex(), row, row)
        self.pixmaps.insert(row, pixmap)
        self.locations.insert(row, location)
        self.endInsertRows()

    def flags(self, index):
        if index.isValid():
            return (Qt.ItemIsEnabled | Qt.ItemIsSelectable |
                    Qt.ItemIsDragEnabled)

        return Qt.ItemIsDropEnabled

    def removeRows(self, row, count, parent):
        if parent.isValid():
            return False

        if row >= len(self.pixmaps) or row + count <= 0:
            return False

        beginRow = max(0, row)
        endRow = min(row + count - 1, len(self.pixmaps) - 1)

        self.beginRemoveRows(parent, beginRow, endRow)

        del self.pixmaps[beginRow:endRow + 1]
        del self.locations[beginRow:endRow + 1]

        self.endRemoveRows()
        return True

    def mimeTypes(self):
        return ['image/x-puzzle-piece']

    def mimeData(self, indexes):
        mimeData = QMimeData()
        encodedData = QByteArray()

        stream = QDataStream(encodedData, QIODevice.WriteOnly)

        for index in indexes:
            if index.isValid():
                pixmap = QPixmap(self.data(index, Qt.UserRole))
                location = self.data(index, Qt.UserRole + 1)
                stream << pixmap << location

        mimeData.setData('image/x-puzzle-piece', encodedData)
        return mimeData

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat('image/x-puzzle-piece'):
            return False

        if action == Qt.IgnoreAction:
            return True

        if column > 0:
            return False

        if not parent.isValid():
            if row < 0:
                endRow = len(self.pixmaps)
            else:
                endRow = min(row, len(self.pixmaps))
        else:
            endRow = parent.row()

        encodedData = data.data('image/x-puzzle-piece')
        stream = QDataStream(encodedData, QIODevice.ReadOnly)

        while not stream.atEnd():
            pixmap = QPixmap()
            location = QPoint()
            stream >> pixmap >> location

            self.beginInsertRows(QModelIndex(), endRow, endRow)
            self.pixmaps.insert(endRow, pixmap)
            self.locations.insert(endRow, location)
            self.endInsertRows()

            endRow += 1

        return True

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        else:
            return len(self.pixmaps)

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def addPieces(self, pixmap):
        self.beginRemoveRows(QModelIndex(), 0, 24)
        #self.pixmaps = []
        #self.locations = []
        self.endRemoveRows()
        self.addPiece(pixmap, QPoint(0, 0))


class DirectoryView(QListView):
    def __init__(self, parent=None):
        super(DirectoryView, self).__init__(parent)
        self.setMinimumSize(600, 400)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(40, 40))
        self.setGridSize(QSize(60, 60))
        self.setMovement(QListView.Snap)
        self.piecePixmaps = []
        self.pieceRects = []
        self.pieceLocations = []
        self.highlightedRect = QRect()
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 400)

    def clear(self):
        self.pieceLocations = []
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QRect()

    def targetSquare(self, position):
        return QRect(position.x() // 80 * 80, position.y() // 80 * 80, 80, 80)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainFrame()
    mainUI.move(60, 60)
    mainUI.show()
    app.exec_()
