from PyQt5 import QtWidgets, QtGui, QtCore


class DirectoryView(QtWidgets.QListView):
    del_request_signal = QtCore.pyqtSignal()
    rename_request_signal = QtCore.pyqtSignal(int)
    new_folder_request_signal = QtCore.pyqtSignal()
    download_request_signal = QtCore.pyqtSignal(QtCore.QModelIndex)
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
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setIconSize(QtCore.QSize(80, 80))
        self.setGridSize(QtCore.QSize(100, 100))
        self.setMovement(QtWidgets.QListView.Snap)
        self.piecePixmaps = []
        self.pieceRects = []
        self.pieceLocations = []
        self.highlightedRect = QtCore.QRect()
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 400)

    def clear(self):
        self.pieceLocations = []
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QtCore.QRect()

    def target_square(self, position):
        return QtCore.QRect(position.x() // 100 * 100, position.y() // 100 * 100, 100, 100)

    def set_directory(self, files):
        self.clear()
        for file in files:
            if file.is_dir:
                self.parent().add_folder_by_directory_entry(file)
            else:
                self.parent().add_file_by_virtual_entry(file)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F2:
            if len(self.selectedIndexes()) == 1:
                self.rename_request_signal.emit(self.selectedIndexes()[0].row())
        if event.key() == QtCore.Qt.Key_Delete:
            self.del_request_signal.emit()

    def popup_menu(self, pos):
        selected_items = self.selectedIndexes()

        menu = QtWidgets.QMenu()
        newFolderAction = QtWidgets.QAction("New folder", None)        #newFolderAction.triggered.connect(something action)
        uploadAction = QtWidgets.QAction("Upload", None)
        downloadAction = QtWidgets.QAction("Download", None)
        renameAction = QtWidgets.QAction("Rename", None)
        deleteAction = QtWidgets.QAction("Delete", None)
        setDirectoryAction = QtWidgets.QAction("Download Directory", None)

        menu.addAction(newFolderAction)
        menu.addSeparator()
        menu.addAction(uploadAction)
        if len(selected_items) > 0:
            menu.addAction(downloadAction)
        menu.addSeparator()
        if len(selected_items) == 1:
            if self.model().files[selected_items[0].row()].is_dir is False:
                menu.addAction(renameAction)
                menu.addSeparator()
        menu.addAction(deleteAction)
        menu.addAction(setDirectoryAction)

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
            self.del_request_signal.emit()