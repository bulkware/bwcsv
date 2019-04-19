# !/usr/bin/env python3
# -*- coding: utf-8 -*-

""" A lightweight application to view CSV files. """

# Python imports
import configparser # Configuration file parser
import os # Miscellaneous operating system interfaces
import sys # System-specific parameters and functions

# Import PyQt modules
from PyQt4 import QtCore, QtGui

# Application classes
from csvparser import CSVParser # A class to handle CSV files

# Application functions
import functions # Useful functions

# Import mainwindow
from mainwindow import *

# Create a class for our mainwindow
class Main(QtGui.QMainWindow):

    # Initialize mainwindow
    def __init__(self):

        # Declare class variables
        self.file = "" # Variable for file
        self.searchresults = [] # A list for search results
        self.fieldseparator = chr(44) # Field separator
        self.textdelimiter = chr(34) # Text delimiter
        self.hheader = True # Boolean for horizontal header
        self.vheader = True # Boolean for vertical header
        self.hlabels = False # Boolean for header labels

        # Create an instance of CSVParser
        self.csvparser = CSVParser()

        # Initialize top level window widget
        QtGui.QMainWindow.__init__(self)

        # This is always the same
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals, menu
        self.ui.actionOpenFile.triggered.connect(self.openFile)
        self.ui.actionFieldSeparator.triggered.connect(self.fieldSeparator)
        self.ui.actionTextDelimiter.triggered.connect(self.textDelimiter)
        self.ui.actionHorizontalHeader.triggered.connect(self.horizontalHeader)
        self.ui.actionVerticalHeader.triggered.connect(self.verticalHeader)
        self.ui.actionHeaderLabels.triggered.connect(self.headerLabels)
        self.ui.actionQuit.triggered.connect(self.quitApplication)
        self.ui.actionAbout.triggered.connect(self.aboutMessage)

        # Connect signals, search
        self.ui.txtSearch.returnPressed.connect(self.searchFromTable)
        self.ui.lstSearchResults.itemClicked.connect(self.selectSearchResult)

        # Drag-and-drop events for file contents table
        self.ui.tblContents.dragEnterEvent = self.dragEnterEvent
        self.ui.tblContents.dragMoveEvent = self.dragEnterEvent
        self.ui.tblContents.dropEvent = self.dropEvent

        # Icons
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.ui.actionOpenFile.setIcon(QtGui.QIcon("open_file.png"))
        self.ui.actionFieldSeparator.setIcon(QtGui.QIcon("fseparator.png"))
        self.ui.actionTextDelimiter.setIcon(QtGui.QIcon("tdelimiter.png"))
        self.ui.actionHorizontalHeader.setIcon(QtGui.QIcon("hheader.png"))
        self.ui.actionVerticalHeader.setIcon(QtGui.QIcon("vheader.png"))
        self.ui.actionHeaderLabels.setIcon(QtGui.QIcon("setheader.png"))
        self.ui.actionQuit.setIcon(QtGui.QIcon("quit.png"))
        self.ui.actionAbout.setIcon(QtGui.QIcon("about.png"))

        # Load settings
        self.loadSettings()

        # Set file if it's in the command line arguments
        if len(sys.argv) > 1:
            if os.path.isfile(sys.argv[1]):
                self.file = sys.argv[1]

        # Set horizontal header to table
        if not self.hheader:
            self.hlabels = False
            self.ui.actionHeaderLabels.setEnabled(False)
            self.ui.actionHorizontalHeader.setChecked(False)
            self.ui.tblContents.horizontalHeader().setVisible(False)

        # Set vertical header to table
        if not self.vheader:
            self.ui.actionVerticalHeader.setChecked(False)
            self.ui.tblContents.verticalHeader().setVisible(False)

        # Set header labels checked
        if self.hlabels:
            self.ui.actionHeaderLabels.setChecked(True)

        # Open CSV file
        if self.file != "":
            self.openCSV(self.file)


    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #+ Actions
    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    # A method to show "open file"-dialog
    def openFile(self):

        # Path to file using a dialog
        file = QtGui.QFileDialog.getOpenFileName(self, "Open CSV file",
            self.file, self.tr("CSV files (*.csv)"))

        # Open file
        if file != "":
            self.openCSV(file)


    # A method to open a CSV file
    def openCSV(self, file):

		# Try to load file
        ok = self.csvparser.load_file(file, self.fieldseparator, 
            self.textdelimiter)
        if ok:
            self.file = file
            self.setWindowTitle("bwCSV - " + os.path.basename(self.file))
            self.ui.statusBar.showMessage(self.csvparser.message)
            self.enableWidgets()
        else:
            self.ui.statusBar.showMessage(self.csvparser.message)
            QtGui.QMessageBox.critical(self, "Error", self.csvparser.message)
            if self.file == "":
                self.disableWidgets()
            return False

        # Populate table widget
        self.refreshTable()


    # Set field separator
    def fieldSeparator(self):

        # Get user input
        fieldseparator, ok = QtGui.QInputDialog.getText(self,
            "Field separator", "Field separator:", 0, self.fieldseparator)

        # If OK was clicked...
        if ok:
            if fieldseparator == "":
                QtGui.QMessageBox.critical(self, "Error",
                    "Field separator cannot be empty.")
                return False

            # Set new field separator
            self.fieldseparator = fieldseparator

            # Reload file if a file is opened
            if self.file != "":
                self.openCSV(self.file)


    # Set text delimiter
    def textDelimiter(self):

        # Get user input
        textdelimiter, ok = QtGui.QInputDialog.getText(self, "Text delimiter",
            "Text delimiter:", 0, self.textdelimiter)

        # If OK was clicked...
        if ok:

            # Set new text delimiter
            self.textdelimiter = textdelimiter

            # Reload file if a file is opened
            if self.file != "":
                self.openCSV(self.file)


    # Show/hide horizontal header
    def horizontalHeader(self):

        if self.ui.actionHorizontalHeader.isChecked():
            self.hheader = True
            self.ui.actionHeaderLabels.setEnabled(True)
            self.ui.tblContents.horizontalHeader().setVisible(True)
        else:
            self.hlabels = False
            self.hheader = False
            self.ui.actionHeaderLabels.setChecked(False)
            self.ui.actionHeaderLabels.setEnabled(False)
            self.ui.actionHorizontalHeader.setChecked(False)
            self.ui.tblContents.horizontalHeader().setVisible(False)

            # Refresh table if a file is opened
            if self.file != "":
                self.refreshTable()


    # Show/hide vertical header
    def verticalHeader(self):

        if self.ui.actionVerticalHeader.isChecked():
            self.vheader = True
            self.ui.tblContents.verticalHeader().setVisible(True)
        else:
            self.vheader = False
            self.ui.tblContents.verticalHeader().setVisible(False)


    # Header labels enable/disable
    def headerLabels(self):

        if self.ui.actionHeaderLabels.isChecked():
            self.hlabels = True
        else:
            self.hlabels = False

        # Refresh table and search if a file is opened
        if self.file != "":
            self.refreshTable()


    # About message
    def aboutMessage(self):
        message = """<strong>bwCSV</strong><br />
        Version 1.2.0<br />
        <br />
        This is free software.<br />
        Released under the General Public License.<br />
        <br />
        <a href="https://github.com/bulkware/bwcsv">GitHub</a>"""
        QtGui.QMessageBox.about(self, "About", message)


    # Quit application
    def quitApplication(self):
        QtGui.QApplication.quit()


    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #+ Events
    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    # Drag
    def dragEnterEvent(self, event):
        if (event.type() == QtCore.QEvent.DragEnter):
            if event.mimeData().hasUrls():
                event.accept()
            else:
                event.ignore()

    # Drop
    def dropEvent(self, event):
        if (event.type() == QtCore.QEvent.Drop):
            if event.mimeData().hasUrls():

                # Take the first item from drag-and-drop and open it
                item = event.mimeData().urls()[0]
                self.openCSV(item.toLocalFile())
                


    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #+ Settings
    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    def loadSettings(self):
        try:
            settings = QtCore.QSettings("bulkware", "bwCSV")
            if settings.contains("geometry"): # Window geometry
                self.restoreGeometry(settings.value("geometry"))
            if settings.contains("state"): # Window state
                self.restoreState(settings.value("state"))
            if settings.contains("file"):
                self.file = settings.value("file", type=str)
            if settings.contains("fieldseparator"):
                self.fieldseparator = settings.value("fieldseparator", type=str)
            if settings.contains("textdelimiter"):
                self.textdelimiter = settings.value("textdelimiter", type=str)
            if settings.contains("horizontalheader"):
                self.hheader = settings.value("horizontalheader", type=bool)
            if settings.contains("verticalheader"):
                self.vheader = settings.value("verticalheader", type=bool)
            if settings.contains("headerlabels"):
                self.hlabels = settings.value("headerlabels", type=bool)
        except:
            self.file = ""
            self.fieldseparator = chr(44)
            self.textdelimiter = chr(34)
            self.hheader = True
            self.vheader = True
            self.hlabels = False
            return False
        else:
            return True


    # Save settings when closing the application
    def closeEvent(self, event):
        settings = QtCore.QSettings("bulkware", "bwCSV")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())
        settings.setValue("file", self.file)
        settings.setValue("fieldseparator", self.fieldseparator)
        settings.setValue("textdelimiter", self.textdelimiter)
        settings.setValue("horizontalheader", self.hheader)
        settings.setValue("verticalheader", self.vheader)
        settings.setValue("headerlabels", self.hlabels)


    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #+ Widgets
    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    # A method to refresh table
    def refreshTable(self):

        # Clear widgets
        self.ui.tblContents.clear()
        self.ui.lstColumns.clear()
        self.ui.lstSearchResults.clear()

        # Count and set columns and rows
        columns = int(self.csvparser.columncount)
        rows = int(self.csvparser.rowcount)

        # If header labels are selected, set the first item to them
        pos1 = None
        pos2 = None
        if self.hheader and self.hlabels:
            pos1 = 1
            rows -= 1
            headers = self.csvparser.filedata[0:1][0]

        # Set columns and rows
        self.ui.tblContents.setColumnCount(columns)
        self.ui.tblContents.setRowCount(rows)

        # Set header labels
        if self.hheader and self.hlabels:
            self.ui.tblContents.setHorizontalHeaderLabels(headers)

        # Populate table widget
        for row, line in enumerate(self.csvparser.filedata[pos1:pos2]):
            for column in range(columns):
                item = QtGui.QTableWidgetItem(line[column])
                item.setFlags(QtCore.Qt.ItemIsSelectable |
                              QtCore.Qt.ItemIsEnabled)
                self.ui.tblContents.setItem(row, column, item)

        # Add columns to column list
        for column in range(columns):
            if self.hheader and self.hlabels:
                self.ui.lstColumns.addItem(headers[column])
            else:
                self.ui.lstColumns.addItem("Column " + str(column + 1))

        # Resize columns and rows to contents
        # setVisible lines are because of QTBUG-9352!
        self.ui.tblContents.setVisible(False)
        self.ui.tblContents.resizeColumnsToContents()
        self.ui.tblContents.resizeRowsToContents()
        self.ui.tblContents.setVisible(True)

        # If search has a string, run search
        searchstring = str(self.ui.txtSearch.text())
        if self.ui.txtSearch.text() != "":
            self.searchFromTable()


    # Search method
    def searchFromTable(self):

        # No file opened
        if self.file == "":
            QtGui.QMessageBox.critical(self, "Error", "No file opened.")
            return False

        # No search string specified
        searchstring = str(self.ui.txtSearch.text())
        if searchstring == "":
            QtGui.QMessageBox.critical(self, "Error",
                "No search string specified.")
            return False

        # Clear search results
        self.searchresults = []
        self.ui.lstSearchResults.clear()

        # Make a list of columns to include in search
        searchcolumns = []
        if len(self.ui.lstColumns.selectedIndexes()) == 0:
            for index in range(self.ui.lstColumns.count()):
                searchcolumns.append(index)
        else:
            for item in self.ui.lstColumns.selectedIndexes():
                searchcolumns.append(item.row())

        # Sort search columns
        searchcolumns.sort()

        # Search for search string in table
        for column in searchcolumns:
            for row in range(self.ui.tblContents.rowCount()):
                item = self.ui.tblContents.item(row, column)
                text = item.text()

                # Case-sensitivity
                if self.ui.chkCaseInsensitive.isChecked():
                    ignorecase = True
                else:
                    ignorecase = False

                # Case-sensitivity
                if self.ui.chkWholeWord.isChecked():
                    wholeword = True
                else:
                    wholeword = False

                # Find match
                if functions.find_string(searchstring, text, ignorecase,
                                        wholeword):
                    self.ui.tblContents.scrollToItem(
                        self.ui.tblContents.item(row, column),
                        QtGui.QAbstractItemView.EnsureVisible)
                    self.ui.lstSearchResults.addItem("Row " + str(row + 1) +
                        ", column " + str(column + 1))
                    self.searchresults.append([row, column])

        # Set first search result selected
        if self.ui.lstSearchResults.count() > 0:
            self.ui.lstSearchResults.setCurrentRow(0)
            self.selectSearchResult()


    # Selecting search result
    def selectSearchResult(self):
        searchcount = int(self.ui.lstSearchResults.count())
        if searchcount > 0:
            row = int(self.ui.lstSearchResults.currentRow())
            pos1 = self.searchresults[row][0]
            pos2 = self.searchresults[row][1]
            self.ui.tblContents.setCurrentCell(pos1, pos2)
            self.ui.tblContents.scrollToItem(
                self.ui.tblContents.item(pos1, pos2),
                QtGui.QAbstractItemView.EnsureVisible)
            self.ui.tblContents.setFocus()


    # Disable widgets
    def disableWidgets(self):
        self.ui.txtSearch.setEnabled(False)
        self.ui.lstColumns.setEnabled(False)
        self.ui.lstSearchResults.setEnabled(False)


    # Enable widgets
    def enableWidgets(self):
        self.ui.txtSearch.setEnabled(True)
        self.ui.lstColumns.setEnabled(True)
        self.ui.lstSearchResults.setEnabled(True)


# Creates an application object and begins the event handling loop
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    ret = app.exec_()
    sys.exit(ret)
