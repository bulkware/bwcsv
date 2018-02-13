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
        self.file = None # Variable for file
        self.searchresults = [] # A list for search results
        self.fieldseparator = chr(44) # Field separator
        self.textdelimiter = chr(34) # Text delimiter
        self.hheader = True # Boolean for horizontal header
        self.vheader = True # Boolean for vertical header
        self.hlabels = False # Boolean for header labels

        # Initialize top level window widget
        QtGui.QMainWindow.__init__(self)

        # This is always the same
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals, menu
        QtCore.QObject.connect(self.ui.menuOpen,
            QtCore.SIGNAL('triggered()'), self.openFile)
        QtCore.QObject.connect(self.ui.menuQuit,
            QtCore.SIGNAL('triggered()'), self.quitApplication)
        QtCore.QObject.connect(self.ui.menuFieldSeparator,
            QtCore.SIGNAL('triggered()'), self.fieldSeparator)
        QtCore.QObject.connect(self.ui.menuTextDelimiter,
            QtCore.SIGNAL('triggered()'), self.textDelimiter)
        QtCore.QObject.connect(self.ui.menuHorizontalHeader,
            QtCore.SIGNAL('triggered()'), self.horizontalHeader)
        QtCore.QObject.connect(self.ui.menuVerticalHeader,
            QtCore.SIGNAL('triggered()'), self.verticalHeader)
        QtCore.QObject.connect(self.ui.menuHeaderLabels,
            QtCore.SIGNAL('triggered()'), self.headerLabels)
        QtCore.QObject.connect(self.ui.menuAboutMessage,
            QtCore.SIGNAL('triggered()'), self.aboutMessage)

        # Connect signals, search
        QtCore.QObject.connect(self.ui.txtSearch,
            QtCore.SIGNAL('returnPressed()'), self.searchFromTable)
        QtCore.QObject.connect(self.ui.lstSearchResults,
            QtCore.SIGNAL("itemClicked (QListWidgetItem *)"),
            self.selectSearchResult)

        # Create an instance of list
        self.csvparser = CSVParser()

        # Load settings
        try:
            settings = QtCore.QSettings("bulkware", "bwCSV")
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
            if settings.contains("windowstate"):
                windowstate = settings.value("windowstate", type=int)
                if windowstate == 1:
                    self.setWindowState(QtCore.Qt.WindowMinimized)
                elif windowstate == 2:
                    self.setWindowState(QtCore.Qt.WindowMaximized)

        # Error occured, set default settings
        except:
            self.file = None
            self.fieldseparator = chr(44)
            self.textdelimiter = chr(34)
            self.hheader = True
            self.vheader = True
            self.hlabels = False

        finally:
            pass

        # Set file if it's in the command line arguments
        if len(sys.argv) > 1:
            if os.path.isfile(sys.argv[1]):
                self.file = sys.argv[1]

        # Set horizontal header to table
        if not self.hheader:
            self.hlabels = False
            self.ui.menuHeaderLabels.setEnabled(False)
            self.ui.menuHorizontalHeader.setChecked(False)
            self.ui.tblContents.horizontalHeader().setVisible(False)

        # Set vertical header to table
        if not self.vheader:
            self.ui.menuVerticalHeader.setChecked(False)
            self.ui.tblContents.verticalHeader().setVisible(False)

        # Set header labels checked
        if self.hlabels:
            self.ui.menuHeaderLabels.setChecked(True)

        # Open CSV file
        if self.file and self.file != "":
            if self.openCSV(self.file):
                pass
            else:
                self.file = None


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
        loadfile = self.csvparser.load_file(file, self.fieldseparator,
                                            self.textdelimiter)
        if loadfile:
            self.file = file
            self.setWindowTitle("bwCSV - " + os.path.basename(self.file))
        else:
            self.ui.statusBar.showMessage(self.csvparser.message)
            QtGui.QMessageBox.critical(self, "Error", self.csvparser.message)
            return False

        # Populate table widget
        if self.refreshTable():
            self.ui.statusBar.showMessage(self.csvparser.message)
            return True
        else:
            message = "Error: unable to refresh table."
            QtGui.QMessageBox.critical(self, "Error", message)
            self.ui.statusBar.showMessage(message)
            return False


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

        # All went well
        return True


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
            if self.file and self.file != "":
                self.openCSV(self.file)


    # Show/hide horizontal header
    def horizontalHeader(self):

        if self.ui.menuHorizontalHeader.isChecked():
            self.hheader = True
            self.ui.menuHeaderLabels.setEnabled(True)
            self.ui.tblContents.horizontalHeader().setVisible(True)
        else:
            self.hlabels = False
            self.hheader = False
            self.ui.menuHeaderLabels.setChecked(False)
            self.ui.menuHeaderLabels.setEnabled(False)
            self.ui.menuHorizontalHeader.setChecked(False)
            self.ui.tblContents.horizontalHeader().setVisible(False)

            # Refresh table if a file is opened
            if self.file and self.file != "":
                self.refreshTable()


    # Show/hide vertical header
    def verticalHeader(self):

        if self.ui.menuVerticalHeader.isChecked():
            self.vheader = True
            self.ui.tblContents.verticalHeader().setVisible(True)
        else:
            self.vheader = False
            self.ui.tblContents.verticalHeader().setVisible(False)


    # Header labels enable/disable
    def headerLabels(self):

        if self.ui.menuHeaderLabels.isChecked():
            self.hlabels = True
        else:
            self.hlabels = False

        # Refresh table and search if a file is opened
        if self.file and self.file != "":
            self.refreshTable()


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


    # About message
    def aboutMessage(self):
        message = """<strong>bwCSV</strong><br />
        Version 1.01<br />
        <br />
        This is free software.<br />
        Released under the General Public Licence.<br />
        <br />
        <a href="http://sourceforge.net/projects/bwcsv/">SourceForge</a>"""
        QtGui.QMessageBox.about(self, "About", message)


    # Closing the application
    def closeEvent(self, event):

        # Save settings
        settings = QtCore.QSettings("bulkware", "bwCSV")
        settings.setValue("file", self.file)
        settings.setValue("fieldseparator", self.fieldseparator)
        settings.setValue("textdelimiter", self.textdelimiter)
        settings.setValue("horizontalheader", self.hheader)
        settings.setValue("verticalheader", self.vheader)
        settings.setValue("headerlabels", self.hlabels)
        settings.setValue("windowstate", int(self.windowState()))


    # Quit application
    def quitApplication(self):
        QtGui.QApplication.quit()


# Creates an application object and begins the event handling loop
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    ret = app.exec_()
    sys.exit(ret)
