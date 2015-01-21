# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flactag_gui.ui'
#
# Created: Mon Jan 19 22:17:01 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(956, 817)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.dirTreeView = QtGui.QTreeView(self.splitter)
        self.dirTreeView.setObjectName(_fromUtf8("dirTreeView"))
        self.fileListView = QtGui.QListView(self.splitter)
        self.fileListView.setObjectName(_fromUtf8("fileListView"))
        self.splitter_2 = QtGui.QSplitter(self.splitter)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.groupBox = QtGui.QGroupBox(self.splitter_2)
        self.groupBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fileNameEdit = QtGui.QLineEdit(self.groupBox)
        self.fileNameEdit.setObjectName(_fromUtf8("fileNameEdit"))
        self.verticalLayout.addWidget(self.fileNameEdit)
        self.sampleRateLabel = QtGui.QLabel(self.groupBox)
        self.sampleRateLabel.setObjectName(_fromUtf8("sampleRateLabel"))
        self.verticalLayout.addWidget(self.sampleRateLabel)
        self.lengthLabel = QtGui.QLabel(self.groupBox)
        self.lengthLabel.setObjectName(_fromUtf8("lengthLabel"))
        self.verticalLayout.addWidget(self.lengthLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.channelsLabel = QtGui.QLabel(self.groupBox)
        self.channelsLabel.setObjectName(_fromUtf8("channelsLabel"))
        self.horizontalLayout.addWidget(self.channelsLabel)
        self.colorLabel = QtGui.QLabel(self.groupBox)
        self.colorLabel.setText(_fromUtf8(""))
        self.colorLabel.setObjectName(_fromUtf8("colorLabel"))
        self.horizontalLayout.addWidget(self.colorLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonAdd = QtGui.QPushButton(self.groupBox)
        self.buttonAdd.setObjectName(_fromUtf8("buttonAdd"))
        self.gridLayout.addWidget(self.buttonAdd, 0, 0, 1, 1)
        self.buttonAddHires = QtGui.QPushButton(self.groupBox)
        self.buttonAddHires.setObjectName(_fromUtf8("buttonAddHires"))
        self.gridLayout.addWidget(self.buttonAddHires, 0, 1, 1, 2)
        self.buttonDelete = QtGui.QPushButton(self.groupBox)
        self.buttonDelete.setObjectName(_fromUtf8("buttonDelete"))
        self.gridLayout.addWidget(self.buttonDelete, 1, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tagListView = QtGui.QTableView(self.splitter_2)
        self.tagListView.setObjectName(_fromUtf8("tagListView"))
        self.verticalLayout_2.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 956, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen_File = QtGui.QAction(MainWindow)
        self.actionOpen_File.setObjectName(_fromUtf8("actionOpen_File"))
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setObjectName(_fromUtf8("action_Save"))
        self.action_Help = QtGui.QAction(MainWindow)
        self.action_Help.setObjectName(_fromUtf8("action_Help"))
        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName(_fromUtf8("action_About"))
        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addAction(self.action_Save)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Quit)
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.action_Help)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "FLAC Tagger", None))
        self.groupBox.setTitle(_translate("MainWindow", "FLAC File", None))
        self.sampleRateLabel.setText(_translate("MainWindow", "Sample rate", None))
        self.lengthLabel.setText(_translate("MainWindow", "Length", None))
        self.channelsLabel.setText(_translate("MainWindow", "Channels", None))
        self.buttonAdd.setToolTip(_translate("MainWindow", "Add new empty tag", None))
        self.buttonAdd.setText(_translate("MainWindow", "Add Tag", None))
        self.buttonAddHires.setToolTip(_translate("MainWindow", "calculate phc tag based on artist and title, add relevant tags", None))
        self.buttonAddHires.setText(_translate("MainWindow", "add HiRes Tags", None))
        self.buttonDelete.setToolTip(_translate("MainWindow", "delete selected tag", None))
        self.buttonDelete.setText(_translate("MainWindow", "Delete Tag", None))
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionOpen_File.setText(_translate("MainWindow", "Open &File", None))
        self.action_Quit.setText(_translate("MainWindow", "&Quit", None))
        self.action_Save.setText(_translate("MainWindow", "&Save", None))
        self.action_Help.setText(_translate("MainWindow", "&Help", None))
        self.action_About.setText(_translate("MainWindow", "&About", None))

