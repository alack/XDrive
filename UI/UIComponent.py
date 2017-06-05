from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pathlib import *
from UniDrive import *


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


class MenuBar(QtWidgets.QFrame):
    drive_remove_signal = QtCore.pyqtSignal(str)
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
        self.drive_actions = QActionGroup(self)
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
        #self.homeBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #self.homeBtn.setText("home!")

        # set folder open btn
        self.folderOpenBtn = QtWidgets.QToolButton()
        self.folderOpenBtn.setIcon(QtGui.QIcon('images/folder_open.png'))

        # set add folder button
        self.addFolderBtn = QtWidgets.QToolButton()
        self.addFolderBtn.setIcon(QtGui.QIcon('images/add_folder_blue.png'))

        # add cloud menu
        self.add_menu_setting()

        # add cloud menu button
        self.addCloudBtn = QtWidgets.QPushButton()
        self.addCloudBtn.setIcon(QtGui.QIcon('images/add_cloud.png'))
        self.addCloudBtn.setMenu(self.addMenu)

        # remove cloud setting
        self.remove_menu_default_setting()

        # remove cloud menu button
        self.removeCloudBtn = QtWidgets.QPushButton()
        self.removeCloudBtn.setIcon(QtGui.QIcon('images/remove_cloud.png'))
        self.removeCloudBtn.setMenu(self.removeMenu)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(self.homeBtn)
        self.layout.addWidget(self.folderOpenBtn)
        self.layout.addWidget(self.addFolderBtn)
        self.layout.addWidget(self.addCloudBtn)
        self.layout.addWidget(self.removeCloudBtn)

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

    def remove_menu_default_setting(self):
        self.removeMenu = QtWidgets.QMenu()

    def remove_menu_add_item(self, item):
        added_action = QAction(str(item[0]+"/"+item[1]), self)
        self.drive_actions.addAction(added_action)
        self.drive_actions.actions()[-1].triggered.connect(
            lambda x: self.drive_remove_each_clicked(added_action, item[1]))
        self.removeMenu.addAction(self.drive_actions.actions()[-1])

    def drive_remove_each_clicked(self, item, name):
        self.removeMenu.removeAction(item)
        del item
        self.drive_remove_signal.emit(name)

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
                background-color: #FFCC00; 
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
                background-color: #99FF66; 
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
        # set horizontal box
        self.hbox = QtWidgets.QHBoxLayout()
        self.setLayout(self.hbox)
        self.hbox.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

    def set_root_button(self):
        for x in self.directoryButtonGroup.buttons():
            x.deleteLater()
            self.directoryButtonGroup.removeButton(x)
        self.add_under_directory_button("/")

    def add_under_directory_button(self, dirName):
        button = QToolButton()
        button.setText(dirName)
        self.directoryButtonGroup.addButton(button)
        self.hbox.addWidget(button)


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

        self.statusIconBtn = QtWidgets.QToolButton()
        self.statusIconBtn.setIcon(QIcon('images/status_ok.png'))
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
        self.statusIconBtn.setIcon(QIcon('images/status_ok.png'))
        self.set_status_label(msg)

    def set_status_wait(self, msg):
        self.statusIconBtn.setIcon(QIcon('images/status_wait.png'))
        self.set_status_label(msg)

    def set_status_fail(self, msg):
        self.statusIconBtn.setIcon(QIcon('images/status_fail.png'))
        self.set_status_label(msg)


class PiecesModel(QAbstractListModel):
    do_rename_signal = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super(PiecesModel, self).__init__(parent)
        self.locations = []
        self.pixmaps = []
        self.files = []# list of DirectoryEntry. instead of self.fineNames

    def clear(self):
        self.locations = []
        self.pixmaps = []
        self.files = []

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if 0 > index.row() or index.row() >= self.rowCount():
            return None
        row = index.row()
        if role == Qt.DisplayRole:
            length = len(self.files[row].name)
            if length >= 8:
                return self.files[row].name[:8]+".."
            return self.files[row].name
        if role == Qt.DecorationRole:
            return QIcon(self.pixmaps[row].scaled(100, 100, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        if role == Qt.EditRole:
            return self.files[row].name
        if role == Qt.ToolTipRole:
            return "Press F2 to change File Name"
        if role == Qt.ForegroundRole:
            return QBrush(QColor(0, 0, 0, 127))
        if role == Qt.UserRole:
            return self.pixmaps[row]
        if role == Qt.UserRole + 1:
            return self.locations[row]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        if 0 > index.row() or index.row() >= self.rowCount():
            return False
        if role == Qt.EditRole:
            if self.files[index.row()].name == value:
                print("not changed")
                return False
            self.do_rename_signal.emit(self.files[index.row()].name, value)
            self.files[index.row()].name = value
            self.dataChanged.emit(index, index)

            return True
        return False

    def add_piece(self, pixmap, location, directory_entry):
        row = len(self.pixmaps)
        self.beginInsertRows(QModelIndex(), row, row)
        self.pixmaps.insert(row, pixmap)
        self.locations.insert(row, location)
        self.files.insert(row, directory_entry)
        self.endInsertRows()
        return row

    def remove_piece(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.pixmaps[row]
        del self.locations[row]
        del self.files[row]
        self.endRemoveRows()

    def flags(self, index):
        return (Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled |
                Qt.ItemIsDropEnabled | Qt.ItemIsEnabled)

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
        del self.files[beginRow:endRow + 1]
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

    def rowCount(self, parent=QModelIndex()):
        return len(self.pixmaps)

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction


class DirectoryView(QListView):
    del_request_signal = QtCore.pyqtSignal(str, int)
    rename_request_signal = QtCore.pyqtSignal(int)
    new_folder_request_signal = QtCore.pyqtSignal()
    download_request_signal = QtCore.pyqtSignal(QModelIndex)
    upload_request_signal = QtCore.pyqtSignal()

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
        self.setIconSize(QSize(80, 80))
        self.setGridSize(QSize(100, 100))
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

    def target_square(self, position):
        return QRect(position.x() // 100 * 100, position.y() // 100 * 100, 100, 100)

    def set_directory(self, files):
        self.clear()
        for file in files:
            if file.is_dir:
                self.parent().add_folder_by_directory_entry(file)
            else:
                self.parent().add_file_by_directory_entry(file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F2:
            for i in self.selectedIndexes():
                self.rename_request_signal.emit(i.row())
        if event.key() == Qt.Key_Delete:
            for i in self.selectedIndexes():
                self.del_request_signal.emit(self.model().files[i.row()].name, i.row())

    def popup_menu(self, pos):
        selected_items = self.selectedIndexes()

        menu = QMenu()
        newFolderAction = QAction("New folder", None)        #newFolderAction.triggered.connect(something action)
        uploadAction = QAction("Upload", None)
        downloadAction = QAction("Download", None)
        renameAction = QAction("Rename", None)
        deleteAction = QAction("Delete", None)

        menu.addAction(newFolderAction)
        menu.addSeparator()
        menu.addAction(uploadAction)
        menu.addAction(downloadAction)
        menu.addSeparator()
        if len(selected_items) == 1:
            if self.model().files[selected_items[0].row()].is_dir is False:
                menu.addAction(renameAction)
                menu.addSeparator()
        menu.addAction(deleteAction)

        action = menu.exec_(self.mapToGlobal(pos))

        if action == newFolderAction:
            self.new_folder_request_signal.emit()
        elif action == uploadAction:
            self.upload_request_signal.emit()
        elif action == downloadAction:
            for i in self.selectedIndexes():
                self.download_request_signal.emit(i)
        elif action == renameAction:
            self.rename_request_signal.emit(selected_items[0].row())
        elif action == deleteAction:
            for i in self.selectedIndexes():
                self.del_request_signal.emit(self.model().files[i.row()].name, i.row())
