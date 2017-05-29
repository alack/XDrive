from exceptions import *
import os
import pathlib
from store import *
import sys
from urllib.parse import urlparse
from UIComponent import *
from UniDrive import UniDrive
import webbrowser


class MainFrame(QtWidgets.QFrame):
    """
        file_tree has directory in dictionary {'directory':'files in directory'}
        file_in_current is file list which are in the current directory
    """
    connected_drive_info = []
    drive_action_list = []
    file_in_current = []
    current_dir = "/"
    totalStoragePercent = 0

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
        self.load_data_from_store_list()
        self.debug = DebugPanel()
        self.debug.move(60, 600)
        self.debug.show()

    def load_data_from_store_list(self):
        # need to get saved store list
        # it's for init
        infos = unidrive.get_store_list()
        for store in infos:
            type = "unknown"
            if store['type'] == "GoogleDriveStore":
                type = "Google"
            if store['type'] == "DropboxStore":
                type = "Dropbox"
            # TODO add box
            item = [type, store['name']]
            self.connected_drive_info.append(item)
            self.m_menuBar.remove_menu_add_item(item)

    def listview_double_clicked(self, idx):
        print("listview_double_clicked")
        """
        clicked_file = self.file_in_current[idx.row()]
        print(clicked_file)
        # TODO if clicked file is directory? go to under directory : ignore
        if clicked_file.is_dir:
            print("folder is clicked")
            temp_dir = [DirectoryEntry("/asdf/bbb", True) for i in range(5)]
            temp_dir.append(DirectoryEntry("asdf", False))
            # TODO get file list of next directory
            self.m_listview.set_directory(temp_dir) #UniDrive.get_list(checked_file)
            # TODO set directory bar
            # TODO set status bar
        """

    def title_bar(self):
        return self.m_titleBar

    def homebtn_clicked(self):
        self.m_directoryBar.set_root_button()
        files = unidrive.get_list("/")
        self.m_listview.set_directory(files)
        self.m_directoryBar.set_root_button()

    def add_drive_menubar_action(self):
        # set trigger to action
        self.m_menuBar.googleAddAction.triggered.connect(self.google_drive_clicked)
        self.m_menuBar.boxAddAction.triggered.connect(self.box_clicked)
        self.m_menuBar.dropboxAddAction.triggered.connect(self.dropbox_clicked)
        self.m_menuBar.homeBtn.clicked.connect(self.homebtn_clicked)

    def google_drive_clicked(self):
        # Get google auth url
        try:
            auth_url = unidrive.register_store('GoogleDriveStore', 'test-googledrive')
            webbrowser.open_new(auth_url)
            res = input('response url for test-googledrive :')
            if unidrive.activate_store('test-googledrive', res):
                self.m_statusBar.set_status_ok()
                self.m_statusBar.statusLabel.setText('success test-googledrive')
                recent_store = unidrive.get_recent_store()
                item = ["Google", recent_store['name']]
                self.connected_drive_info.append(item)
                self.m_menuBar.remove_menu_add_item(item)
            else:
                self.m_statusBar.set_status_fail()
                self.m_statusBar.statusLabel.setText('fail test-googledrive')
        except Exception:
            self.m_statusBar.set_status_fail()
            self.m_statusBar.statusLabel.setText('test-googledrive is already registered')

    def box_clicked(self):
        # TODO need to write code about box get auth_url
        # TODO delete Item from
        item = ["box", "highalps", "z9123rnaz00cxv"]
        self.m_statusBar.set_status_label("box Added, ("+item[0]+", "+item[1]+", "+item[2]+")")
        # TODO delete Item to

    def dropbox_clicked(self):
        # get dropbox auth_url
        try:
            auth_url = unidrive.register_store('DropboxStore', 'test-dropbox')
            webbrowser.open_new(auth_url)
            res = input('response url for test-dropbox :')
            if unidrive.activate_store('test-dropbox', res):
                self.m_statusBar.set_status_ok()
                self.m_statusBar.statusLabel.setText('success test-dropbox')
                recent_store = unidrive.get_recent_store()
                item = ["Google", recent_store['name']]
                self.connected_drive_info.append(item)
                self.m_menuBar.remove_menu_add_item(item)
            else:
                self.m_statusBar.set_status_fail()
                self.m_statusBar.statusLabel.setText('fail test-dropbox')
        except Exception:
            self.m_statusBar.set_status_fail()
            self.m_statusBar.statusLabel.setText('test-googledrive is already registered')

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
            self.totalStoragePercent += count
            if self.totalStoragePercent > 100:
                self.totalStoragePercent = 100
            self.m_menuBar.set_progressbar(self.totalStoragePercent)
            if count >= 2:
                status = str(count)+" files are uploading"
                self.m_statusBar.set_status_label(status)
            elif count == 1:
                status = str(upload_list[0].toLocalFile())
                self.m_statusBar.set_status_label(str(upload_list[0].toLocalFile())+" is uploading")
            for url in upload_list:
                path = urlparse(url.toLocalFile()).path
                cur_path = Path(path)
                if cur_path.is_dir():
                    self.add_folder_by_url(cur_path)
                    UniDrive.make_directory(cur_path, cur_path.stem)
                else:
                    self.add_file_by_url(path)
                    if cur_path.is_file() is False:
                        self.m_statusBar.set_status_fail()
                        self.m_statusBar.statusLabel.setText('file does not exists')
                        continue
                    with open(cur_path, 'rb') as src_file:
                        src_data = src_file.read()
                    try:
                        unidrive.upload_file(path, src_data)
                    except BaseStoreException as e:
                        self.m_statusBar.set_status_fail()
                        self.m_statusBar.statusLabel.setText(cur_path+' upload error')
                    else:
                        self.m_statusBar.set_status_ok()
                        self.m_statusBar.statusLabel.setText('Upload Done')
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

    def add_file_by_url(self, path):
        path = Path(path)
        fileName = path.stem
        ext = path.suffix
        if ext == ".pdf":
            image = QPixmap('images/pdf.png')
        elif ext == ".png" or ext == '.jpg' or ext == '.jpeg':
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
        row = self.model.add_piece(image, QPoint(0, 0))
        # TODO it's for test.
        # delete this variable
        info = DirectoryEntry(fileName)
        print(info)
        self.file_in_current.append(info)

    def add_file_by_directory_entry(self, file):
        name = file.name
        ext = str(name).split('.')
        ext = ext[-1]
        if len(ext) == 1:
            fileName = ext[0]
        else:
            fileName = name[:len(name) - len(ext)]
            ext = ".unknown"
        if ext == ".pdf":
            image = QPixmap('images/pdf.png')
        elif ext == ".png" or ext == '.jpg' or ext == '.jpeg':
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
        row = self.model.add_piece(image, QPoint(0, 0))
        # TODO it's for test.
        # delete this variable
        info = DirectoryEntry(fileName)
        self.file_in_current.append(info)

    def add_folder_by_url(self, path):
        try:
            path = Path(path)
            folder_name = path.stem
            image = QPixmap('images/folder.png')
            row = self.model.add_piece(image, QPoint(0, 0))

            # TODO it's for test.
            # delete this variable
            info = DirectoryEntry(folder_name)
            info.is_dir = True
            self.file_in_current.append(info)
            #TODO upload under all directory is future plan
#            self.add_under_directory(path, next_dir)
        except PermissionError:
            pass

    def add_folder_by_directory_entry(self, folder):
        try:
            image = QPixmap('images/folder.png')
            row = self.model.add_piece(image, QPoint(0, 0))
            self.file_in_current.append(folder)
        except PermissionError:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    prjdir = pathlib.Path('.').resolve()
    unidrive = UniDrive(prjdir)

    mainUI = MainFrame()
    mainUI.move(60, 0)
    mainUI.show()

    app.exec_()
