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
    download_dir = ""
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
        self.m_menuBar.addFolderBtn.clicked.connect(self.add_folder_btn_action)
        self.m_menuBar.folderOpenBtn.clicked.connect(self.folder_open_btn_action)

        self.m_statusBar = StatusBar()
        self.m_listview = DirectoryView()
        self.m_listview.doubleClicked.connect(self.listview_double_clicked)
        self.m_listview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.m_listview.setDragDropMode(QAbstractItemView.DragDrop)
        self.m_listview.key_pressed_signal.connect(self.listview_del_pressed)

        self.model = PiecesModel()
        self.m_listview.setModel(self.model)
        self.m_directoryBar = DirectoryBar()
        self.m_directoryBar.directoryButtonGroup.buttonClicked[QAbstractButton].connect(
            self.go_specific_directory_button)

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
        self.load_root_files()

    def listview_del_pressed(self, filename, row):
        unidrive.remove_file(self.current_dir+filename)
        self.model.remove_piece(row)
        for i, item in enumerate(self.file_in_current):
            if item.name == filename:
                del(self.file_in_current[i])
                break


    def folder_open_btn_action(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.download_dir = folder

    def add_folder_btn_action(self):
        image = QPixmap('images/folder.png')
        last_idx = len(self.model.files)
        default_folder_name = "newFolder"
        newFolderName = "newFolder"
        num = 1
        while True:
            exit_flag = 0
            for item in self.model.files:
                if item.is_dir is True:
                    if newFolderName == item.name:
                        newFolderName = default_folder_name + "(" + str(num) + ")"
                        num += 1
                        exit_flag = 1
            if exit_flag == 0:
                break
        unidrive.make_directory(self.current_dir, newFolderName)
        self.add_folder_by_directory_entry(DirectoryEntry(newFolderName, True))

    def go_specific_directory_button(self, button):
        flag = 0
        clicked_path = ""
        next_dir = ""
        for i, x in enumerate(self.m_directoryBar.directoryButtonGroup.buttons()):
            if flag == 1:
                x.deleteLater()
                self.m_directoryBar.directoryButtonGroup.removeButton(x)
            else:
                if i <= 1:
                    clicked_path += x.text()
                else:
                    clicked_path += "/"+x.text()
            if x == button:
                flag = 1
                next_dir = x.text()
        self.current_dir = clicked_path
        self.dir_selected(next_dir, True)

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

    def dir_selected(self, name, isFromDirectoryBar):
        nextlist = unidrive.get_list(self.current_dir)
        self.file_in_current = nextlist[0:]
        self.model.clear()
        if isFromDirectoryBar == False:
            if self.current_dir == '/':
                self.m_directoryBar.set_root_button()
            else:
                self.m_directoryBar.add_under_directory_button(name)
        self.m_listview.clear()
        if len(nextlist) != 0:
            self.m_listview.set_directory(nextlist)

    def listview_double_clicked(self, idx):
        clicked_file = self.model.files[idx.row()]
        path = Path(clicked_file.name)
        fileName = path.stem
        ext = path.suffix
        if clicked_file.is_dir:
            self.current_dir = self.current_dir + clicked_file.name + "/"
            self.dir_selected(clicked_file.name, False)
        # TODO when user do doubleClick file? downlaod : not
        else:
            if self.download_dir == "":
                self.m_statusBar.set_status_fail("Need to set download directory")
            elif os.path.exists(self.download_dir) is False:
                self.m_statusBar.set_status_fail("Download directory is not exists")
            else:
                name_num = 1
                while os.path.exists(self.download_dir + "/" + fileName + ext):
                    fileName = path.stem + "(" + str(name_num) + ")"
                    name_num += 1
                downed_data = unidrive.download_file(self.current_dir+clicked_file.name)
                print(downed_data)
                # TODO : if file is existed ? "new" + filename
                with open(self.download_dir+"/"+fileName+ext, 'wb') as outfile:
                    outfile.write(downed_data)
                self.m_statusBar.set_status_ok("Download Done. "+self.download_dir+"/"+fileName+ext)

    def title_bar(self):
        return self.m_titleBar

    def homebtn_clicked(self):
        self.load_root_files()

    def load_root_files(self):
        self.current_dir = "/"
        self.dir_selected("/", False)

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
                self.m_statusBar.set_status_ok("Success test-googledrive")
                recent_store = unidrive.get_recent_store()
                item = ["Google", recent_store['name']]
                self.connected_drive_info.append(item)
                self.m_menuBar.remove_menu_add_item(item)
            else:
                self.m_statusBar.set_status_fail("Fail test-googledrive")
        except Exception:
            self.m_statusBar.set_status_fail("tesg-googledrive is alread registered")

    def box_clicked(self):
        # TODO need to write code about box get auth_url
        # TODO delete Item from
        item = ["box", "highalps", "z9123rnaz00cxv"]
        self.m_statusBar.set_status_ok("box Added, ("+item[0]+", "+item[1]+", "+item[2]+")")
        # TODO delete Item to

    def dropbox_clicked(self):
        # get dropbox auth_url
        try:
            auth_url = unidrive.register_store('DropboxStore', 'test-dropbox')
            webbrowser.open_new(auth_url)
            res = input('response url for test-dropbox :')
            if unidrive.activate_store('test-dropbox', res):
                self.m_statusBar.set_status_ok("Success test-dropbox")
                recent_store = unidrive.get_recent_store()
                item = ["Google", recent_store['name']]
                self.connected_drive_info.append(item)
                self.m_menuBar.remove_menu_add_item(item)
            else:
                self.m_statusBar.set_status_fail("Fail test-dropbox")
        except Exception:
            self.m_statusBar.set_status_fail("Test-googledrive is already registered")

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
                self.m_statusBar.set_status_ok(status)
            elif count == 1:
                status = str(upload_list[0].toLocalFile())
                self.m_statusBar.set_status_ok(str(upload_list[0].toLocalFile())+" is uploading")
            for url in upload_list:
                path = urlparse(url.toLocalFile()).path
                cur_path = Path(path)
                if cur_path.is_dir():
                    unidrive.make_directory(self.current_dir, cur_path.stem)
                    self.add_folder_by_url(cur_path)
                else:
                    self.add_file_by_url(path)
                    if cur_path.is_file() is False:
                        self.m_statusBar.set_status_fail("file does not exists")
                        continue
                    with open(cur_path, 'rb') as src_file:
                        src_data = src_file.read()
                    try:
                        unidrive.upload_file(self.current_dir+cur_path.name, src_data)

                    except BaseStoreException as e:
                        self.m_statusBar.set_status_fail(cur_path+" upload error")
                    else:
                        self.m_statusBar.set_status_ok("Upload Done.")
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

    def ext_to_QPixmap(self, ext):
        if ext == ".pdf" or ext == ".pptx":
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
        return image

    def add_file_by_url(self, path):
        path = Path(path)
        fileName = path.stem
        ext = path.suffix
        image = self.ext_to_QPixmap(ext)
        last_idx = len(self.model.files)
        row = self.model.add_piece(image, QPoint(last_idx, 0), DirectoryEntry(fileName+ext, False))
        # TODO it's for test.
        # delete this variable
        info = DirectoryEntry(fileName)
        self.file_in_current.append(info)

    def add_file_by_directory_entry(self, file):
        path = Path(file.name)
        fileName = path.stem
        ext = path.suffix
        image = self.ext_to_QPixmap(ext)
        last_idx = len(self.model.files)
        row = self.model.add_piece(image, QPoint(last_idx, 0), DirectoryEntry(fileName+ext, False))
        # TODO it's for test.
        # delete this variable
        info = DirectoryEntry(fileName)
        self.file_in_current.append(info)

    def add_folder_by_url(self, path):
        try:
            path = Path(path)
            folder_name = path.stem
            image = QPixmap('images/folder.png')
            last_idx = len(self.model.files)
            row = self.model.add_piece(image, QPoint(last_idx, 0), DirectoryEntry(folder_name, True))

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
            last_idx = len(self.model.files)
            row = self.model.add_piece(image, QPoint(last_idx, 0), DirectoryEntry(folder.name, True))
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
