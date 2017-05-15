import sys
import os
from urllib.parse import urlparse
from os.path import splitext
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

current_files = []


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
        debugPanel.textEdit.insertPlainText("arrange button clicked\n")

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


class DirectoryBar(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # set css for TitleBar
        css = """
        QWidget{
            Background: #FFFFFF;
            border-radius: 1px;
            color: black;
        }
        """
        # set css and background
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)

        self.directoryButtonGroup = QButtonGroup()
        self.directoryButtonGroup.buttonClicked[QAbstractButton].connect(self.on_directory_button_clicked)
        # set horizontal box
        self.hbox = QtWidgets.QHBoxLayout()
        self.setLayout(self.hbox)
        self.hbox.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.set_home_button()
        self.add_under_directory_button("1")
        self.add_under_directory_button("2")
        self.add_under_directory_button("3")
        self.add_under_directory_button("4")
        self.add_under_directory_button("5")

    def set_home_button(self):
        for x in self.directoryButtonGroup.buttons():
            self.del_under_directory_button(x)
        self.add_under_directory_button("home")

    def add_under_directory_button(self, dirName):
        button = QToolButton()
        button.setText(dirName)
        self.directoryButtonGroup.addButton(button)
        self.hbox.addWidget(button)

    def del_under_directory_button(self, button):
        button.deleteLater()
        self.directoryButtonGroup.removeButton(button)

    def go_specific_directory_button(self, button):
        flag = 0
        for x in self.directoryButtonGroup.buttons():
            if flag == 1:
                self.del_under_directory_button(x)
            if x == button:
                flag = 1

    def on_directory_button_clicked(self, button):
        self.go_specific_directory_button(button)


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
        """
        self.setStyleSheet(css)
        self.m_mouse_down = False
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(800, 500)
        self.setAcceptDrops(True)

        self.m_titleBar = TitleBar()
        self.m_menuBar = MenuBar()
        self.m_statusBar = StatusBar()
        self.m_listview = DirectoryView()
        self.m_listview.doubleClicked.connect(self.listview_double_clicked)
        self.model = PiecesModel()
        self.m_listview.setModel(self.model)
        self.m_directoryBar = DirectoryBar()

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.addWidget(self.m_menuBar)
        vbox.addWidget(self.m_directoryBar)
        vbox.addWidget(self.m_listview)
        vbox.addWidget(self.m_statusBar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.menubar_action()

    def listview_double_clicked(self, icons):
        image = QPixmap('images/unknown.png')
        self.model.add_piece(image, QPoint(0, 0))
        """
        need to correct
        """

    def title_bar(self):
        return self.m_titleBar

    def menubar_action(self):
        # set trigger to action
        self.m_menuBar.googleAddAction.triggered.connect(self.google_drive_clicked)
        self.m_menuBar.boxAddAction.triggered.connect(self.box_clicked)
        self.m_menuBar.dropboxAddAction.triggered.connect(self.dropbox_clicked)
        self.m_menuBar.homeBtn.clicked.connect(self.homebtn_clicked)

    def homebtn_clicked(self):
        self.m_directoryBar.set_home_button()

    def google_drive_clicked(self):
        debugPanel.textEdit.insertPlainText("google drive clicked in google_drive_clicked\n")
        self.m_statusBar.statusLabel.setText("Google Added")
        # do something with browser
        # get return value

    def box_clicked(self):
        debugPanel.textEdit.insertPlainText("box clicked in box_clicked\n")
        self.m_statusBar.statusLabel.setText("Box Added")
        # do something with browser
        # get return value

    def dropbox_clicked(self):
        debugPanel.textEdit.insertPlainText("dropbox clicked in dropbox_clicked\n")
        self.m_statusBar.statusLabel.setText("Dropbox Added")
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
                debugPanel.textEdit.insertPlainText("file url : "+str(url.toLocalFile())+"\n")
                path = urlparse(url.toLocalFile()).path
                if os.path.isdir(path):
                    self.add_folder(path)
                else:
                    self.add_icons(path)

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

    def add_icons(self, path):
        splits = path.split("/")
        splitLen = len(splits)
        #fileName = splits[splitLen - 1]
        #ext = splitext(path)[1]
        ext = os.path.splitext(path)[-1]
        print(ext)
        if ext == ".pdf":
            image = QPixmap('images/pdf.png')
        elif ext == ".png" or ext == '.jpg' or ext == '.jpeg' or ext == '.jpeg':
            image = QPixmap('images/png.png')
        elif ext == '.zip':
            image = QPixmap('images/zip.png')
        elif ext == '.txt':
            image = QPixmap('images/txt.png')
        elif ext == '.mp4':
            image = QPixmap('images/mp4.png')
        elif ext == '.java':
            image = QPixmap('images/java.png')
        elif ext == '.xlsx' or ext == '.xls':
            image = QPixmap('images/xlsx.png')
        elif ext == '.py':
            image = QPixmap('images/py.png')
        elif ext == '.docx' or ext == '.rtf':
            image = QPixmap('images/docx.png')
        else:
            image = QPixmap('images/unknown.png')
        self.model.add_piece(image, QPoint(0, 0))
        file_info = []
        file_info.append(path)
        file_info.append(ext)
        current_files.append(file_info)

    def add_folder(self, path):
        try:
            folder_name = os.path.split(path)[-1]
            debugPanel.textEdit.insertPlainText("In add_folder, folder name : "+folder_name+"\n")
            image = QPixmap('images/folder.png')
            self.model.add_piece(image, QPoint(0, 0))
            file_names = os.listdir(path)
            for file in file_names:
                sibling = os.path.join(path, file)
                if os.path.isdir(sibling):
                    self.add_folder(sibling)
                else:
                    debugPanel.textEdit.insertPlainText(path + " : not folder\n")
        except PermissionError:
            pass


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

    def add_piece(self, pixmap, location):
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


class DirectoryView(QListView):
    def __init__(self, parent=None):
        super(DirectoryView, self).__init__(parent)
        css = """
        QListView{
            Background: #FFFFFF;
            color:white;
            font:13px ;
            font-weight:bold;
        }
        """
        self.setStyleSheet(css)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(40, 40))
        self.setGridSize(QSize(60, 60))
        self.setMovement(QListView.Snap)
        self.piecePixmaps = []
        self.pieceRects = []
        self.pieceLocations = []
        self.iconNames = []
        self.highlightedRect = QRect()
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 400)

    def clear(self):
        self.pieceLocations = []
        self.piecePixmaps = []
        self.pieceRects = []
        self.iconNames = []
        self.highlightedRect = QRect()

    def targetSquare(self, position):
        return QRect(position.x() // 60 * 60, position.y() // 60 * 60, 60, 60)


class DebugPanel(QFrame):
    def __init__(self, parent=None):
        super(DebugPanel, self).__init__(parent)
        self.setMinimumSize(800, 300)
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        self.textEdit = QPlainTextEdit()
        layout.addWidget(self.textEdit)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainFrame()
    mainUI.move(60, 0)
    mainUI.show()
    debugPanel = DebugPanel()
    debugPanel.move(60, 600)
    debugPanel.show()
    app.exec_()
