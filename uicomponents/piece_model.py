from PyQt5 import QtGui, QtCore, QtWidgets
from pathlib import Path


class PiecesModel(QtCore.QAbstractListModel):
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

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if 0 > index.row() or index.row() >= self.rowCount():
            return None
        row = index.row()
        if role == QtCore.Qt.DisplayRole:
            selected = self.files[row].name
            length = len(selected)
            if length > 8:
                return selected[:8]+".."
            return selected
        if role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(self.pixmaps[row].scaled(100, 100, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation))
        if role == QtCore.Qt.EditRole:
            selected = self.files[row]
            if selected.is_dir is False:
                path = Path(selected.name)
                fileName = path.stem
                return fileName
            return None
        if role == QtCore.Qt.ToolTipRole:
            return self.files[row].name
        if role == QtCore.Qt.ForegroundRole:
            return QtGui.QBrush(QtGui.QColor(0, 0, 0, 127))
        if role == QtCore.Qt.UserRole:
            return self.pixmaps[row]
        if role == QtCore.Qt.UserRole + 1:
            return self.locations[row]
        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False
        if 0 > index.row() or index.row() >= self.rowCount():
            return False
        if role == QtCore.Qt.EditRole:
            before = self.files[index.row()]
            path = Path(before.name)
            fileName = path.stem
            if fileName == value:
                return False
            if value == "" or len(value) > 200:
                return False
            self.do_rename_signal.emit(before.name, value + path.suffix)
            self.files[index.row()].name = value + path.suffix
            self.dataChanged.emit(index, index)
            return True
        return False

    def add_piece(self, pixmap, location, directory_entry):
        row = len(self.pixmaps)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.pixmaps.insert(row, pixmap)
        self.locations.insert(row, location)
        self.files.insert(row, directory_entry)
        self.endInsertRows()
        return row

    def remove_piece(self, row):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        del self.pixmaps[row]
        del self.locations[row]
        del self.files[row]
        self.endRemoveRows()

    def flags(self, index):
        return (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled |
                QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEnabled)

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
        mimeData = QtCore.QMimeData()
        encodedData = QtCore.QByteArray()

        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.WriteOnly)
        for index in indexes:
            if index.isValid():
                pixmap = QtGui.QPixmap(self.data(index, QtCore.Qt.UserRole))
                location = self.data(index, QtCore.Qt.UserRole + 1)
                stream << pixmap << location
        mimeData.setData('image/x-puzzle-piece', encodedData)
        return mimeData

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat('image/x-puzzle-piece'):
            return False

        if action == QtCore.Qt.IgnoreAction:
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
        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.ReadOnly)

        while not stream.atEnd():
            pixmap = QtGui.QPixmap()
            location = QtGui.QPoint()
            stream >> pixmap >> location

            self.beginInsertRows(QtCore.QModelIndex(), endRow, endRow)
            self.pixmaps.insert(endRow, pixmap)
            self.locations.insert(endRow, location)
            self.endInsertRows()

            endRow += 1

        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.pixmaps)

    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction
