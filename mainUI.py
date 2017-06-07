import os
import sys
import webbrowser
from PyQt5 import QtGui, QtCore, QtWidgets
from UniDrive import UniDrive
from uicomponents import *
from exceptions import *
from store import DirectoryEntry
from pathlib import Path


class MainFrame(QtWidgets.QFrame):
    connected_drive_info = []
    file_in_current = []
    current_dir = "/"
    download_dir = ""

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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMinimumSize(800, 500)
        self.setAcceptDrops(True)
        self.m_titleBar = TitleBar()
        self.m_menuBar = MenuBar()
        self.m_menuBar.addFolderBtn.clicked.connect(self.add_folder_action)
        self.m_menuBar.drive_remove_signal.connect(self.drive_remove_pressed)

        self.m_menuBar.googleAddAction.triggered.connect(self.google_drive_clicked)
        self.m_menuBar.boxAddAction.triggered.connect(self.box_clicked)
        self.m_menuBar.dropboxAddAction.triggered.connect(self.dropbox_clicked)
        self.m_menuBar.homeBtn.clicked.connect(self.load_files_from_root)

        self.m_statusBar = StatusBar()

        self.m_listview = DirectoryView()
        self.m_listview.customContextMenuRequested.connect(self.m_listview.popup_menu)
        self.m_listview.doubleClicked.connect(self.list_view_double_clicked)
        self.m_listview.del_request_signal.connect(self.listview_del_pressed)
        self.m_listview.rename_request_signal.connect(self.listview_f2_pressed)
        self.m_listview.new_folder_request_signal.connect(self.add_folder_action)
        self.m_listview.download_request_signal.connect(self.list_view_double_clicked)
        self.m_listview.upload_request_signal.connect(self.listview_upload_clicked)

        self.model = PiecesModel()
        self.model.do_rename_signal.connect(self.do_rename)
        self.model.drop_piece_signal.connect(self.move_to_folder)

        self.m_listview.setModel(self.model)
        self.m_directoryBar = DirectoryBar()
        self.m_directoryBar.directoryButtonGroup.buttonClicked[QtWidgets.QAbstractButton].connect(
            self.go_specific_directory_button)

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.addWidget(self.m_menuBar)
        vbox.addWidget(self.m_directoryBar)
        vbox.addWidget(self.m_listview)
        vbox.addWidget(self.m_statusBar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        self.load_data_from_store_list()
        self.load_files_from_root()

    def move_to_folder(self, next_folder: str):
        idx = self.m_listview.selectedIndexes()[0]
        filename = self.model.files[idx.row()].name
        print(self.current_dir + filename + "->" + self.current_dir + next_folder + "/" + filename)
        self.do_rename(filename, next_folder + "/" + filename)

    def listview_upload_clicked(self):
        files = QtWidgets.QFileDialog.getOpenFileNames()
        for path in files[0]:
            self.download_progress(path)

    def drive_remove_pressed(self, selected):
        unidrive.remove_store(selected)

    def listview_del_pressed(self):
        while len(self.m_listview.selectedIndexes()):
            idx = self.m_listview.selectedIndexes()[0]
            if self.model.files[idx.row()].is_dir is False:
                filename = self.model.files[idx.row()].name
                unidrive.remove_file(self.current_dir+filename)
            else:
                filename = self.model.files[idx.row()].name
                unidrive.remove_directory(self.current_dir + filename)
            self.model.remove_piece(idx.row())
            for i, item in enumerate(self.file_in_current):
                if item.name == filename:
                    del(self.file_in_current[i])
                    break
        self.set_progress_to_usage()

    def listview_f2_pressed(self, row):
        idx = self.m_listview.model().index(row, 0, QtCore.QModelIndex())
        self.m_listview.setCurrentIndex(idx)
        self.m_listview.edit(idx)

    def do_rename(self, before, after):
        unidrive.rename(self.current_dir+before, self.current_dir+after)
        for file in self.file_in_current:
            if file.name == before:
                file.name = after
                break

    def set_download_directory_action(self):
        self.download_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")

    def add_folder_action(self):
        image = QtGui.QPixmap('images/exts/folder.png')
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
        self.add_folder_by_virtual_entry(VirtualEntry(DirectoryEntry(newFolderName, True)))

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
        infos = unidrive.get_store_list()
        for store in infos:
            type = "unknown"
            if store['type'] == "GoogleDriveStore":
                type = "GoogleDrive"
            elif store['type'] == "DropboxStore":
                type = "Dropbox"
            elif store['type'] == "BoxStore":
                type = "Box"
            item = [type, store['name']]
            self.connected_drive_info.append(item)
            self.m_menuBar.remove_menu_add_item(item)

    def dir_selected(self, name, is_from_director_bar):
        next_list = VirtualEntry.list_to_virtual(unidrive.get_list(self.current_dir))
        self.file_in_current = next_list[:]
        self.model.clear()
        if is_from_director_bar is False:
            if self.current_dir == '/':
                self.m_directoryBar.set_root_button()
            else:
                self.m_directoryBar.add_under_directory_button(name)
        self.m_listview.clear()
        if len(next_list) != 0:
            self.m_listview.set_directory(next_list)

    def list_view_double_clicked(self, idx):
        clicked_file = self.model.files[idx.row()]
        fileName = clicked_file.pure_name
        ext = clicked_file.ext
        if clicked_file.is_dir:
            self.current_dir = self.current_dir + clicked_file.name + "/"
            self.dir_selected(clicked_file.name, False)
        else:
            self.m_statusBar.set_status_wait("Downloading...")
            self.set_download_directory_action()
            if os.path.exists(self.download_dir) is False:
                self.m_statusBar.set_status_fail("Download directory is not exists")
                return
            else:
                name_num = 1
                while os.path.exists(self.download_dir + "/" + fileName + ext):
                    fileName = clicked_file.pure_name + "(" + str(name_num) + ")"
                    name_num += 1
                downed_data = unidrive.download_file(self.current_dir+clicked_file.name)

                with open(self.download_dir+"/"+fileName+ext, 'wb') as outfile:
                    outfile.write(downed_data)

                self.m_statusBar.set_status_ok("Download Done. "+self.download_dir+"/"+fileName+ext)

    def load_files_from_root(self):
        self.current_dir = "/"
        self.dir_selected("/", False)

    def drive_addtion(self, type: str):
        try:
            init_drive_name = type
            name_num = 1
            while [type, init_drive_name] in self.connected_drive_info:
                init_drive_name = type + str(name_num)
                name_num += 1
            auth_url = unidrive.register_store(type+'Store', init_drive_name)
            webbrowser.open_new(auth_url)
            res = input('response url for ' + init_drive_name + ' : ')
            if unidrive.activate_store(init_drive_name, res):
                self.m_statusBar.set_status_ok("Success " + init_drive_name)
                recent_store = unidrive.get_store_list()[-1]
                item = [type, recent_store['name']]
                self.connected_drive_info.append(item)
                self.m_menuBar.remove_menu_add_item(item)
            else:
                self.m_statusBar.set_status_fail("Fail " + init_drive_name)
        except Exception:
            self.m_statusBar.set_status_fail(init_drive_name + "is alread registered")

    def google_drive_clicked(self):
        self.drive_addtion("GoogleDrive")

    def box_clicked(self):
        # TODO need to write code about box get auth_url
        # TODO delete Item from
        item = ["box", "highalps", "z9123rnaz00cxv"]
        self.m_statusBar.set_status_ok("box Added, ("+item[0]+", "+item[1]+", "+item[2]+")")
        # TODO delete Item to

    def dropbox_clicked(self):
        self.drive_addtion("Dropbox")

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
        elif event.mimeData().hasFormat('image/x-puzzle-piece'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            upload_list = event.mimeData().urls()
            count = len(upload_list)
            if count >= 2:
                status = str(count)+" files are uploading"
                self.m_statusBar.set_status_wait(status)
            elif count == 1:
                status = str(upload_list[0].toLocalFile())
                self.m_statusBar.set_status_wait(str(upload_list[0].toLocalFile())+" is uploading")
            for url in upload_list:
                path = str(Path(url.toLocalFile()))
                self.download_progress(path)
        else:
            self.m_listview.highlightedRect = QtCore.QRect()
            event.ignore()

    def download_progress(self, path):
            cur_path = Path(path)
            if cur_path.is_dir():
                unidrive.make_directory(self.current_dir, cur_path.stem)
                self.add_folder_by_url(cur_path)
            else:
                self.add_file_by_url(path)
                if cur_path.is_file() is False:
                    self.m_statusBar.set_status_fail("file does not exists")
                    return
                with open(cur_path, 'rb') as src_file:
                    src_data = src_file.read()
                try:
                    if unidrive.upload_file(self.current_dir + cur_path.name, src_data) is True:
                        self.m_statusBar.set_status_ok(str(path) + " is uploaded")
                    else:
                        self.m_statusBar.set_status_ok(str(path) + " upload failed")
                except BaseStoreException as e:
                    self.m_statusBar.set_status_fail(str(cur_path) + " upload error")
                else:
                    self.m_statusBar.set_status_ok("Upload Done.")

    def find_piece(self, pieceRect):
        try:
            return self.m_listview.pieceRects.index(pieceRect)
        except ValueError:
            return -1

    def mouseReleaseEvent(self, event):
        m_mouse_down = False

    def mousePressEvent(self, event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = (event.button() == QtCore.Qt.LeftButton)

    def ext_to_QPixmap(self, ext):
        path = 'images/exts/'+ext[1:]+".png"
        if os.path.exists(path) is False:
            image = QtGui.QPixmap('images/exts/unknown.png')
        else:
            image = QtGui.QPixmap(path)
        return image

    def add_file_by_url(self, path):
        path = Path(path)
        fileName = path.stem
        ext = path.suffix
        image = self.ext_to_QPixmap(ext)
        last_idx = len(self.model.files)
        row = self.model.add_piece(image, QtCore.QPoint(last_idx, 0),
                                   VirtualEntry(DirectoryEntry(fileName+ext, False)))
        # TODO it's for test.
        # delete this variable
        info = VirtualEntry(DirectoryEntry(fileName))
        self.file_in_current.append(info)
        self.set_progress_to_usage()

    def add_file_by_virtual_entry(self, file: VirtualEntry):
        fileName = file.pure_name
        ext = file.ext
        image = self.ext_to_QPixmap(ext)
        last_idx = len(self.model.files)
        self.model.add_piece(image, QtCore.QPoint(last_idx, 0), file)

        self.file_in_current.append(file)
        self.set_progress_to_usage()

    def add_folder_by_url(self, path):
        try:
            path = Path(path)
            folder_name = path.stem
            image = QtGui.QPixmap('images/exts/folder.png')
            last_idx = len(self.model.files)
            current = VirtualEntry(DirectoryEntry(folder_name, True))
            self.model.add_piece(image, QtCore.QPoint(last_idx, 0), current)

            self.file_in_current.append(current)

            #TODO upload under all directory is future plan
            #self.add_under_directory(path, next_dir)
            self.set_progress_to_usage()
        except PermissionError:
            pass

    def add_folder_by_virtual_entry(self, folder):
        try:
            image = QtGui.QPixmap('images/exts/folder.png')
            last_idx = len(self.model.files)
            self.model.add_piece(image, QtCore.QPoint(last_idx, 0), folder)
            self.file_in_current.append(folder)
            self.set_progress_to_usage()
        except PermissionError:
            pass

    def set_progress_to_usage(self):
        res = unidrive.get_usage()
        limit = 0
        used = 0
        for x in res:
            used += x['used']
            limit += x['limit']
        self.m_menuBar.set_progressbar(used, limit)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    splash_pix = QtGui.QPixmap('images/loading.png')
    splash_pix_resized = splash_pix.scaled(1000, 800, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
    splash = QtWidgets.QSplashScreen(splash_pix_resized, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    prjdir = Path('.').resolve()
    unidrive = UniDrive(prjdir)

    mainUI = MainFrame()
    mainUI.move(60, 60)
    mainUI.show()
    splash.finish(mainUI)

    app.exec_()
