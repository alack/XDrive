from PyQt5 import QtWidgets, QtGui, QtCore


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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)

        self.directoryButtonGroup = QtWidgets.QButtonGroup()
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
        button = QtWidgets.QToolButton()
        button.setText(dirName)
        self.directoryButtonGroup.addButton(button)
        self.hbox.addWidget(button)

