#!/usr/bin/python
# -*- coding: utf-8 -*-

""" A lightweight application to view CSV-files. """

# Python imports
import configparser # Configuration file parser
import os # Miscellaneous operating system interfaces
import sys # System-specific parameters and functions

# Import PyQt modules
from PyQt4 import QtCore, QtGui

# Application classes
from csvparser import CSVParser # A class to handle CSV-files

# Application functions
import functions # Useful functions

# Import mainwindow
from mainwindow import *

# Create a class for our mainwindow
class Main(QtGui.QMainWindow):

    # Initialize mainwindow
    def __init__(self):

        # Declare class variables
        self.configfile = "config.cfg" # Configuration file
        self.searchresults = [] # A list for search results
        self.filepath = "" # String for opened filename and path
        self.fieldseparator = chr(44) # Field separator
        self.textdelimiter = chr(34) # Text delimiter
        self.horizontalheader = True # Boolean for horizontal header
        self.verticalheader = True # Boolean for vertical header
        self.headerlabels = False # Boolean for header labels

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

        # Load configuration file
        if os.path.isfile(self.configfile):
            if self.loadConfig():
                message = "Configuration file loaded successfully."
            else:
                message = "Error: unable to load configuration file."

            # Show message
            self.ui.statusBar.showMessage(message)

        # Set file if it's in the command line arguments
        if len(sys.argv) > 1:
            if os.path.isfile(sys.argv[1]):
                self.filepath = sys.argv[1]

        # Set horizontal header to table
        if not self.horizontalheader:
            self.headerlabels = False
            self.ui.menuHeaderLabels.setEnabled(False)
            self.ui.menuHorizontalHeader.setChecked(False)
            self.ui.tblContents.horizontalHeader().setVisible(False)

        # Set vertical header to table
        if not self.verticalheader:
            self.ui.menuVerticalHeader.setChecked(False)
            self.ui.tblContents.verticalHeader().setVisible(False)

        # Set header labels checked
        if self.headerlabels:
            self.ui.menuHeaderLabels.setChecked(True)

        # Open CSV-file
        if self.filepath != "":
            if self.openCSV(self.filepath):
                pass
            else:
                self.filepath = ""


    # Load configuration file
    def loadConfig(self):

        # Try to load configuration file
        try:
            config = configparser.RawConfigParser()
            config.read(self.configfile)

            self.filepath = str(config.get("default",
                "file path"))
            self.fieldseparator = str(config.get("default",
                "field separator"))
            self.textdelimiter = str(config.get("default",
                "text delimiter"))
            self.horizontalheader = config.getboolean("default",
                "horizontal header")
            self.verticalheader = config.getboolean("default",
                "vertical header")
            self.headerlabels = config.getboolean("default",
                "header labels")

            windowstate = config.getint("default", "window state")
            if windowstate == 1:
                self.setWindowState(QtCore.Qt.WindowMinimized)
            elif windowstate == 2:
                self.setWindowState(QtCore.Qt.WindowMaximized)

            # If field separator is empty, set default
            if self.fieldseparator == "":
                self.fieldseparator = chr(44)

            # Discard variables
            if config: del(config)

        # Except
        except:
            return(False)

        # Finally
        finally:
            return(True)


    # Save configuration file
    def saveConfig(self):

        # Try to save configuration file
        try:
            config = configparser.RawConfigParser()

            config.add_section("default")
            config.set("default", "file path", self.filepath)
            config.set("default", "field separator", self.fieldseparator)
            config.set("default", "text delimiter", self.textdelimiter)
            config.set("default", "horizontal header", self.horizontalheader)
            config.set("default", "vertical header", self.verticalheader)
            config.set("default", "header labels", self.headerlabels)
            config.set("default", "window state", int(self.windowState()))

            with open(self.configfile, "w") as configfile:
                config.write(configfile)

            # Discard variables
            if config: del(config)

        # Except
        except:
            return(False)

        # Finally
        finally:
            return(True)


     # A method to show "open file"-dialog
    def openFile(self):

        # Path to file using a dialog
        filepath = QtGui.QFileDialog.getOpenFileName(self, "Open CSV file",
            self.filepath, self.tr("CSV files (*.csv)"))

        # Open file
        if filepath != "":
            self.openCSV(filepath)


    # A method to open a csv-file
    def openCSV(self, filepath):

		# Try to load file
        loadfile = self.csvparser.load_file(filepath, self.fieldseparator,
                                            self.textdelimiter)
        if loadfile:
            self.filepath = filepath
            self.ui.statusBar.showMessage(self.csvparser.message)
        else:
            self.ui.statusBar.showMessage(self.csvparser.message)
            QtGui.QMessageBox.critical(self, "Error", self.csvparser.message)
            return(False)

        # Populate table widget
        if self.refreshTable():
            return(True)
        else:
            return(False)


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
        if self.horizontalheader and self.headerlabels:
            pos1 = 1
            rows -= 1
            headers = self.csvparser.filedata[0:1][0]

        # Set columns and rows
        self.ui.tblContents.setColumnCount(columns)
        self.ui.tblContents.setRowCount(rows)

        # Set header labels
        if self.horizontalheader and self.headerlabels:
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
            if self.horizontalheader and self.headerlabels:
                self.ui.lstColumns.addItem(headers[column])
            else:
                self.ui.lstColumns.addItem("Column " + str(column + 1))

        # Resize columns and rows to contents
        # setVisible lines are because of QTBUG-9352!
        self.ui.tblContents.setVisible(False)
        self.ui.tblContents.resizeColumnsToContents()
        self.ui.tblContents.resizeRowsToContents()
        self.ui.tblContents.setVisible(True)

        # All went well
        return(True)


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
                return(False)

            # Set new field separator
            self.fieldseparator = fieldseparator

            # Reload file if a file is opened
            if self.filepath != "":
                self.openCSV(self.filepath)


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
            if self.filepath != "":
                self.openCSV(self.filepath)


    # Show/hide horizontal header
    def horizontalHeader(self):

        if self.ui.menuHorizontalHeader.isChecked():
            self.horizontalheader = True
            self.ui.menuHeaderLabels.setEnabled(True)
            self.ui.tblContents.horizontalHeader().setVisible(True)
        else:
            self.headerlabels = False
            self.horizontalheader = False
            self.ui.menuHeaderLabels.setChecked(False)
            self.ui.menuHeaderLabels.setEnabled(False)
            self.ui.menuHorizontalHeader.setChecked(False)
            self.ui.tblContents.horizontalHeader().setVisible(False)

            # Refresh table if a file is opened
            if self.filepath != "":
                self.refreshTable()


    # Show/hide vertical header
    def verticalHeader(self):

        if self.ui.menuVerticalHeader.isChecked():
            self.verticalheader = True
            self.ui.tblContents.verticalHeader().setVisible(True)
        else:
            self.verticalheader = False
            self.ui.tblContents.verticalHeader().setVisible(False)


    # Header labels enable/disable
    def headerLabels(self):

        if self.ui.menuHeaderLabels.isChecked():
            self.headerlabels = True
        else:
            self.headerlabels = False

        # Refresh table if a file is opened
        if self.filepath != "":
            self.refreshTable()


    # Search method
    def searchFromTable(self):

        # No file opened
        if self.filepath == "":
            QtGui.QMessageBox.critical(self, "Error", "No file opened.")
            return(False)

        # No search string specified
        searchstring = str(self.ui.txtSearch.text())
        if searchstring == "":
            QtGui.QMessageBox.critical(self, "Error",
                "No search string specified.")
            return(False)

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
        message = "<strong>bwCSV</strong><br />"
        message += "Version 1.00<br />"
        message += "<br />"
        message += "This is free software.<br />"
        message += "Released under the General Public Licence.<br />"
        QtGui.QMessageBox.about(self, "About", message)


    # Closing the application
    def closeEvent(self, event):

        # Save configuration file
        if self.saveConfig():
            pass
        else:
            QtGui.QMessageBox.critical(self, "Error",
                "Unable to save configuration file.")


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
