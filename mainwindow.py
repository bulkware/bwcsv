# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Wed Feb 26 15:52:44 2014
#      by: PyQt4 UI code generator 4.10.3
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
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.tblContents = QtGui.QTableWidget(self.centralwidget)
        self.tblContents.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblContents.sizePolicy().hasHeightForWidth())
        self.tblContents.setSizePolicy(sizePolicy)
        self.tblContents.setAcceptDrops(True)
        self.tblContents.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblContents.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblContents.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tblContents.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tblContents.setWordWrap(False)
        self.tblContents.setObjectName(_fromUtf8("tblContents"))
        self.tblContents.setColumnCount(0)
        self.tblContents.setRowCount(0)
        self.tblContents.horizontalHeader().setVisible(True)
        self.tblContents.verticalHeader().setVisible(True)
        self.horizontalLayout_3.addWidget(self.tblContents)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(15, -1, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblSearch = QtGui.QLabel(self.centralwidget)
        self.lblSearch.setMinimumSize(QtCore.QSize(200, 0))
        self.lblSearch.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lblSearch.setObjectName(_fromUtf8("lblSearch"))
        self.verticalLayout.addWidget(self.lblSearch)
        self.txtSearch = QtGui.QLineEdit(self.centralwidget)
        self.txtSearch.setEnabled(False)
        self.txtSearch.setMinimumSize(QtCore.QSize(200, 0))
        self.txtSearch.setMaximumSize(QtCore.QSize(200, 16777215))
        self.txtSearch.setObjectName(_fromUtf8("txtSearch"))
        self.verticalLayout.addWidget(self.txtSearch)
        self.chkCaseInsensitive = QtGui.QCheckBox(self.centralwidget)
        self.chkCaseInsensitive.setMinimumSize(QtCore.QSize(200, 0))
        self.chkCaseInsensitive.setMaximumSize(QtCore.QSize(200, 16777215))
        self.chkCaseInsensitive.setChecked(True)
        self.chkCaseInsensitive.setObjectName(_fromUtf8("chkCaseInsensitive"))
        self.verticalLayout.addWidget(self.chkCaseInsensitive)
        self.chkWholeWord = QtGui.QCheckBox(self.centralwidget)
        self.chkWholeWord.setObjectName(_fromUtf8("chkWholeWord"))
        self.verticalLayout.addWidget(self.chkWholeWord)
        spacerItem = QtGui.QSpacerItem(200, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.lblColumns = QtGui.QLabel(self.centralwidget)
        self.lblColumns.setMinimumSize(QtCore.QSize(200, 0))
        self.lblColumns.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lblColumns.setObjectName(_fromUtf8("lblColumns"))
        self.verticalLayout.addWidget(self.lblColumns)
        self.lstColumns = QtGui.QListWidget(self.centralwidget)
        self.lstColumns.setEnabled(False)
        self.lstColumns.setMinimumSize(QtCore.QSize(200, 0))
        self.lstColumns.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lstColumns.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.lstColumns.setObjectName(_fromUtf8("lstColumns"))
        self.verticalLayout.addWidget(self.lstColumns)
        spacerItem1 = QtGui.QSpacerItem(200, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.lblResults = QtGui.QLabel(self.centralwidget)
        self.lblResults.setMinimumSize(QtCore.QSize(200, 0))
        self.lblResults.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lblResults.setObjectName(_fromUtf8("lblResults"))
        self.verticalLayout.addWidget(self.lblResults)
        self.lstSearchResults = QtGui.QListWidget(self.centralwidget)
        self.lstSearchResults.setEnabled(False)
        self.lstSearchResults.setMinimumSize(QtCore.QSize(200, 0))
        self.lstSearchResults.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lstSearchResults.setObjectName(_fromUtf8("lstSearchResults"))
        self.verticalLayout.addWidget(self.lstSearchResults)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSettings = QtGui.QMenu(self.menuBar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionOpenFile = QtGui.QAction(MainWindow)
        self.actionOpenFile.setObjectName(_fromUtf8("actionOpenFile"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setMenuRole(QtGui.QAction.TextHeuristicRole)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionFieldSeparator = QtGui.QAction(MainWindow)
        self.actionFieldSeparator.setObjectName(_fromUtf8("actionFieldSeparator"))
        self.actionTextDelimiter = QtGui.QAction(MainWindow)
        self.actionTextDelimiter.setObjectName(_fromUtf8("actionTextDelimiter"))
        self.actionVerticalHeader = QtGui.QAction(MainWindow)
        self.actionVerticalHeader.setCheckable(True)
        self.actionVerticalHeader.setChecked(True)
        self.actionVerticalHeader.setObjectName(_fromUtf8("actionVerticalHeader"))
        self.actionHorizontalHeader = QtGui.QAction(MainWindow)
        self.actionHorizontalHeader.setCheckable(True)
        self.actionHorizontalHeader.setChecked(True)
        self.actionHorizontalHeader.setObjectName(_fromUtf8("actionHorizontalHeader"))
        self.actionHeaderLabels = QtGui.QAction(MainWindow)
        self.actionHeaderLabels.setCheckable(True)
        self.actionHeaderLabels.setObjectName(_fromUtf8("actionHeaderLabels"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuFile.addAction(self.actionOpenFile)
        self.menuFile.addAction(self.actionQuit)
        self.menuSettings.addAction(self.actionFieldSeparator)
        self.menuSettings.addAction(self.actionTextDelimiter)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionHorizontalHeader)
        self.menuSettings.addAction(self.actionVerticalHeader)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionHeaderLabels)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tblContents, self.txtSearch)
        MainWindow.setTabOrder(self.txtSearch, self.chkCaseInsensitive)
        MainWindow.setTabOrder(self.chkCaseInsensitive, self.lstColumns)
        MainWindow.setTabOrder(self.lstColumns, self.lstSearchResults)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "bwCSV", None))
        self.lblSearch.setText(_translate("MainWindow", "Search:", None))
        self.chkCaseInsensitive.setText(_translate("MainWindow", "Case insensitive", None))
        self.chkWholeWord.setText(_translate("MainWindow", "Whole word search", None))
        self.lblColumns.setText(_translate("MainWindow", "Search columns:", None))
        self.lblResults.setText(_translate("MainWindow", "Search results:", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionOpenFile.setText(_translate("MainWindow", "Open file...", None))
        self.actionOpenFile.setToolTip(_translate("MainWindow", "Open file...", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionQuit.setToolTip(_translate("MainWindow", "Quit", None))
        self.actionFieldSeparator.setText(_translate("MainWindow", "Field separator...", None))
        self.actionTextDelimiter.setText(_translate("MainWindow", "Text delimiter...", None))
        self.actionVerticalHeader.setText(_translate("MainWindow", "Vertical header", None))
        self.actionHorizontalHeader.setText(_translate("MainWindow", "Horizontal header", None))
        self.actionHeaderLabels.setText(_translate("MainWindow", "Set header labels from first line", None))
        self.actionAbout.setText(_translate("MainWindow", "About...", None))
        self.actionAbout.setToolTip(_translate("MainWindow", "About...", None))

