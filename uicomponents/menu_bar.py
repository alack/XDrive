from PyQt5 import QtWidgets, QtGui, QtCore


class MenuBar(QtWidgets.QFrame):
    drive_remove_signal = QtCore.pyqtSignal(str)
    to_kilo = 1024
    to_mega = to_kilo*1024
    to_giga = to_mega * 1024

    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
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
        self.drive_actions = QtWidgets.QActionGroup(self)
        # set css and background
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)

        # add/remove cloud, setting, arrange button
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setValue(0)  # default
        self.progressBar.setTextVisible(True)

        # set home button
        self.homeBtn = QtWidgets.QToolButton()
        self.homeBtn.setIcon(QtGui.QIcon('images/menuIcons/home.png'))
        #self.homeBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #self.homeBtn.setText("home!")

        # set add folder button
        self.addFolderBtn = QtWidgets.QToolButton()
        self.addFolderBtn.setIcon(QtGui.QIcon('images/menuIcons/add_folder.png'))

        self.refreshBtn = QtWidgets.QToolButton()
        self.refreshBtn.setIcon(QtGui.QIcon('images/menuIcons/refresh.png'))

        # add cloud menu
        self.add_menu_setting()

        # add cloud menu button
        self.addCloudBtn = QtWidgets.QPushButton()
        self.addCloudBtn.setIcon(QtGui.QIcon('images/menuIcons/add_cloud.png'))
        self.addCloudBtn.setMenu(self.addMenu)

        # remove cloud setting
        self.remove_menu_default_setting()

        # remove cloud menu button
        self.removeCloudBtn = QtWidgets.QPushButton()
        self.removeCloudBtn.setIcon(QtGui.QIcon('images/menuIcons/remove_cloud.png'))
        self.removeCloudBtn.setMenu(self.removeMenu)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(self.homeBtn)
        self.layout.addWidget(self.refreshBtn)
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
        self.googleAddAction = QtWidgets.QAction(QtGui.QIcon('images/driveIcons/google_small.png'), 'GoogleDrive', self)
        self.boxAddAction = QtWidgets.QAction(QtGui.QIcon('images/driveIcons/box.png'), "Box", self)
        self.dropboxAddAction = QtWidgets.QAction(QtGui.QIcon('images/driveIcons/dropbox.png'), "Dropbox", self)

        self.addMenu.addAction(self.googleAddAction)
        self.addMenu.addAction(self.boxAddAction)
        self.addMenu.addAction(self.dropboxAddAction)

    def remove_menu_default_setting(self):
        self.removeMenu = QtWidgets.QMenu()

    def remove_menu_add_item(self, item):
        added_action = QtWidgets.QAction(str(item[0]+"/"+item[1]), self)
        self.drive_actions.addAction(added_action)
        self.drive_actions.actions()[-1].triggered.connect(
            lambda x: self.drive_remove_each_clicked(added_action, item[1]))
        self.removeMenu.addAction(self.drive_actions.actions()[-1])

    def drive_remove_each_clicked(self, item, name):
        self.removeMenu.removeAction(item)
        del item
        self.drive_remove_signal.emit(name)

    # progressbar's color, percent
    def set_progressbar(self, res):
        limit = 0
        used = 0
        for x in res:
            used += x['used']
            limit += x['limit']
        value = 0
        if limit > 0:
            value = (used*100)/limit
        self.progressBar.setValue(value)
        self.progressBar.setFormat("%.2lf GB / %.2lf GB  %.2lf %%" %(used/self.to_giga, limit/self.to_giga, value))

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
