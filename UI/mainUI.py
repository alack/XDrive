import sys
import os
from urllib.parse import urlparse
from UIComponent import *
from drivetest.web2 import *




class MainFrame(QtWidgets.QFrame):
    current_files = []
    connected_drive_info = []
    drive_action_list = []
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
        self.add_drive_menubar_action()

    def listview_double_clicked(self, icons):
        image = QPixmap('images/unknown.png')
        self.model.add_piece(image, QPoint(0, 0))
        """
        need to correct
        """

    def title_bar(self):
        return self.m_titleBar

    def homebtn_clicked(self):
        self.m_directoryBar.set_home_button()

    def add_drive_menubar_action(self):
        # set trigger to action
        self.m_menuBar.googleAddAction.triggered.connect(self.google_drive_clicked)
        self.m_menuBar.boxAddAction.triggered.connect(self.box_clicked)
        self.m_menuBar.dropboxAddAction.triggered.connect(self.dropbox_clicked)
        self.m_menuBar.homeBtn.clicked.connect(self.homebtn_clicked)

    def google_drive_clicked(self):
        print("google drive clicked in google_drive_clicked\n")
        self.m_statusBar.set_status_label("Google Added")
        item = ["google", "djsc023401", "key"]
        self.connected_drive_info.append(item)
        self.m_menuBar.remove_menu_add_item(item)

        # do something with browser
        # get return value

    def box_clicked(self):
        print("box clicked in box_clicked\n")
        self.m_statusBar.set_status_label("Box Added")
        # do something with browser
        # get return value

    def dropbox_clicked(self):
        print("dropbox clicked in dropbox_clicked\n")
        self.m_statusBar.set_status_label("Dropbox Added")
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
                self.m_statusBar.set_status_label(status)
            elif count == 1:
                status = str(upload_list[0].toLocalFile())
                self.m_statusBar.set_status_label(str(upload_list[0].toLocalFile())+" is uploading")
            for url in upload_list:
                print("file url : "+str(url.toLocalFile())+"\n")
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
        self.current_files.append(file_info)

    def add_folder(self, path):
        try:
            folder_name = os.path.split(path)[-1]
            print("In add_folder, folder name : "+folder_name+"\n")
            image = QPixmap('images/folder.png')
            self.model.add_piece(image, QPoint(0, 0))
            file_names = os.listdir(path)
            for file in file_names:
                sibling = os.path.join(path, file)
                if os.path.isdir(sibling):
                    self.add_folder(sibling)
                else:
                    print(path + " : not folder\n")
        except PermissionError:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    mainUI = MainFrame()
    mainUI.move(60, 0)
    mainUI.show()
    app.exec_()
